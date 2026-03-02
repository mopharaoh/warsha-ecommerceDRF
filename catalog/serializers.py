from rest_framework import serializers
from .models import Product ,ProductImage,ProductVariant,Category
from django.db import transaction
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = '__all__'
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value

    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than Zero.")
        return value
        
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

class ProductCreateSerializer(serializers.ModelSerializer):
    variants=VariantSerializer(many=True)
    images=ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name','category','brand','description','variants','images']

    def create(self, validated_data):
        variants_data=validated_data.pop('variants')
        images_data=validated_data.pop('images')
        with transaction.atomic():
            product = Product.objects.create(**validated_data)
            for variant in variants_data:
                variant.pop('product', None)
                ProductVariant.objects.create(product=product,**variant)
            for image in images_data:
                image.pop('product', None)
                ProductImage.objects.create(product=product,**image)

        return product
    
    def validate_variants(self,value):
        if not value:
            raise serializers.ValidationError('Product must have at least one variant.')
        return value
        
#Nested Update 
# class ProductUpdateSerializer(serializers.ModelSerializer):
#     variants=VariantSerializer(many=True)
#     images=ImageSerializer(many=True)

#     class Meta:
#         model = Product
#         fields = ['name','category','brand','description','variants','images']
#     def update(self, instance, validated_data):
#         variants_data = validated_data.pop('variants',[])
#         images_data = validated_data.pop('images',[])

#         instance.name=validated_data.get('name',instance.name)
#         instance.category=validated_data.get('category',instance.category)
#         instance.brand=validated_data.get('brand',instance.brand)
#         instance.description=validated_data.get('description',instance.description)
#         instance.save()

#         existing_variants = {v.id: v for v in instance.variants.all()}
#         for variant_data in variants_data:
#             variant_id = variant_data.get('id',None)

#             if variant_id and variant_id in existing_variants:
#                 variant = existing_variants[variant_id]
                
#                 for attr , value in variant_id.items():
#                     setattr(variant,attr,value)
#                 variant.save()
#             else:
#                 ProductVariant.objects.create(product=instance,**variant_data)

#         existing_images = {img.id: img for img in instance.images.all()}

#         for image_data in images_data:
#             image_id = image_data.get('id', None)

#             if image_id and image_id in existing_images:
#                 image = existing_images[image_id]
#                 image.image = image_data.get('image', image.image)
#                 image.save()
#             else:
#                 ProductImage.objects.create(product=instance, **image_data)     
#         return instance