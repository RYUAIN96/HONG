from rest_framework import serializers
from .models import Item # 모델에서 당겨서 제이선 사용 가능 모델과 직렬화 되는 것

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('no', 'name', 'price', 'regdate')

        # 아이템이라는 오브젝트가 들어오면 필드로 내용을 바꾸겠다는 의미