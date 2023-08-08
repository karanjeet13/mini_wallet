from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from mywallet.models import Customer, Transactions, Wallet
from mywallet.serializers import TransactionSerializer, WalletSerializer


class ItemAlreadyExists(Exception):
    pass


@api_view(["POST"])
def initiate_wallet(request):
    if request.method == "POST":
        customer_xid = request.data.get("customer_xid")
        try:
            customer = Customer.objects.get(customer_xid=customer_xid)
            wallet = Wallet.objects.filter(customer=customer).last()
            if wallet:
                raise ItemAlreadyExists ("Wallet Already Exists")
            wallet = Wallet.objects.create(customer=customer)
            return Response({
                "data": {
                    "token": Token.objects.get(user=customer.user).key
                },
                "status": "success"
            })
        except ItemAlreadyExists as e:
            return Response({"data": {"error": "Wallet already Exists"}, "status": "fail"})
        except Exception as e:
            response = {
                "data": {
                    "error": {
                    "customer_xid": [ "Missing data for required field."]}},
                "status": "fail"}
            return Response(response)


@api_view(["GET","POST","PATCH"])
@authentication_classes([TokenAuthentication])
def wallet_actions(request):
    status = "fail"
    try:
        wallet = Wallet.objects.filter(customer__user=request.user).last()
        if request.method == "GET":
            data = {"error": "Wallet disabled"}
            if wallet.is_active:
                status = "success"
                data = {"wallet": WalletSerializer(wallet).data}
                
        if request.method == "POST":
            data= {"error": "Already enabled"}
            if not wallet.is_active:
                wallet.is_active = True
                wallet.save(update_fields=["is_active"])
                status= "success"
                data={"wallet": WalletSerializer(wallet).data}
        
        if request.method == "PATCH":
            wallet.is_active = False
            status = "success"
            wallet.save(update_fields=["is_active"])
    
    except Exception:
        data = {"message": "no wallet found"}
            
    return Response(
        {
            "status": status,
            "data": data
        }
    )


@api_view(["POST", "GET"])
@authentication_classes([TokenAuthentication])
def wallet_transactions(request, operation):
    if request.method == "GET" and operation == "transactions":
        status = "fail"
        try:
            wallet_ids = Wallet.objects.filter(customer__user=request.user).values_list(
                "id", flat=True)
            transactions = Transactions.objects.filter(wallet_id__in=wallet_ids).all()
            status = "success"
            data = {
                "transactions": [TransactionSerializer(transaction).data for \
                                  transaction in transactions]
            }
        except Exception:
            data = {"error": "Wallet disabled"}
        return Response({
            "status": status,
            "data": data
        })

    if request.method == "POST":
        status = "fail"
        try:
            amount = request.data.get("amount")
            reference_id = request.data.get("reference_id")
            wallet = Wallet.objects.filter(id=reference_id, customer__user=request.user).last()
            if operation == "deposits":
                wallet.balance+=int(amount)
            else:
                wallet.balance-=int(amount)
            wallet.save(update_fields=["balance"])
            transaction = Transactions.objects.create(
                amount = amount, status="success", transaction_type="deposit", wallet=wallet)
            status="success"
            data = {
                "deposit": TransactionSerializer(transaction).data
            }
        except Exception:
            data = {"message": "error occured or wrong wallet credentials"}
        return Response({"status": status, "data": data})