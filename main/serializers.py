from rest_framework import serializers
from .models import *


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image',)


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'author')

    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES
        problem = Problem.objects.create(
            author=request.user,
            **validated_data
        )
        for picture in pictures_files.getlist('pictures'):
            Picture.objects.create(
                image=picture,
                problem=problem
            )
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.pictures.all().delete()
        for image in images_data.getlist('pictures'):
            Picture.objects.create(image=image, problem=instance)
        return instance

    # request.user
    # Problem.objects.create(
    #     author=request.user
    # )
    #
    # request.FILES -> [1, 2, 3, 4, 5] -> 2
    # for i in [1, 2, 3, 4, 5]:
    #     Picture.objects.create(
    #         image=i,
    #         problem=problem
    #     )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pictures'] = PictureSerializer(  # пережают все картинки
            instance.pictures.all(), many=True
        ).data
        action = self.context.get('action')
        print('------------------------------')
        print(instance.replies.all())
        print('------------------------------')
        if action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        elif action == 'list':
            representation['replies'] = instance.replies.count()
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user, **validated_data
        )
        return reply

        # self.context.get('action') -> 'list', 'get', 'destroy', 'partial'

        # {       # вложный JSON
        #     'hello': 1,
        #     'author': 'email@gmail.com',
        #     'text': 'Text',
        #     'pictures': {
        #         'picture': 'link',
        #         'picture': 'Link',
        #         ...
        #     }
        # }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment

