from rest_framework import serializers

from styleshines.models import User,Jewellery,JewelleryVarients,Cart,Orders,Offers,Review

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password","phone","address"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class OfferSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    discount_price=serializers.CharField(read_only=True)
    start_date=serializers.CharField(read_only=True)
    end_date=serializers.CharField(read_only=True)
    class Meta:
        model=Offers
        exclude=("jewel_varient",)
        
class JewelleryVarientSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    offers=OfferSerializer(many=True,read_only=True)
    class Meta:
        model=JewelleryVarients
        exclude=("jewel",)
        # fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    jewel=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields="__all__"

class JewellerySerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)
    # category=serializers.SlugRelatedField(read_only=True,slug_field="name")
    varients=JewelleryVarientSerializer(many=True,read_only=True)
    reviews=ReviewSerializer(many=True,read_only=True)
    avg_rating=serializers.CharField(read_only=True)

    class Meta:
        model=Jewellery
        fields="__all__"   

class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    jewel_varient=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Cart
        fields=["id","jewel_varient","user","status","date"]

class OrderSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    jewel_varient=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    orderd_date=serializers.CharField(read_only=True)
    expected_date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Orders
        fields="__all__"
