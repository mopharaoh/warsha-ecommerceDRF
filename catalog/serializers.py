from rest_framework import serializers
from .models import Product ,ProductImage,ProductVariant,Category

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = "__all__"
class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    variants=VariantSerializer(many=True,read_only=True)
    images=ImageSerializer(many=True,read_only=True)
    

    class Meta:
        model=Product
        fields = ['id','name','brand','description','variants','images']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

# class ProductCreateSerializer(serializers.ModelSerializer):
#     variants=VariantSerializer(many=True)
#     images=ImageSerializer(many=True)

#     def create(self, validated_data):
#         var=validated_data.pop(self.variants)
#         img=validated_data.pop(self.images)
#         Product.objects.create(**self.validated_data)
#         for v in self.variants:
#             ProductVariant.objects.create(**validated_data)
#         for i in self.images:
#             ProductImage.objects.create(**validated_data)
        
    
