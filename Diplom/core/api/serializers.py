from collections import OrderedDict
from rest_framework import serializers

from ..models import Image, Author, Entity, AuthorAlias, AuthorsSpecialization


class PrimaryKeySerializerField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super(PrimaryKeySerializerField, self).__init__(**kwargs)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                super(PrimaryKeySerializerField, self).to_representation(item),
                super(PrimaryKeySerializerField, self).display_value(item)
            )
            for item in queryset
        ])

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        serializer = self.serializer(value, context=self.context)
        serializer.parent = self.parent
        return serializer.data


class ImageURLField(serializers.URLField):
    def to_representation(self, value):
        if value:
            return value.image.url
        else: return ""


class ImageSpecializationSerializer(serializers.ModelSerializer):
    image = serializers.SlugRelatedField(read_only=True, slug_field='name_ru')
    image_api_link = serializers.HyperlinkedIdentityField(view_name='image-detail', source='image_id')
    image_front_link = serializers.HyperlinkedIdentityField(view_name='image-detail-front', source='image_id')
    specialization = serializers.ChoiceField(choices=AuthorsSpecialization.SPECIALIZATIONS, source='get_specialization_display')

    class Meta:
        model = AuthorsSpecialization
        fields = ('image', 'image_api_link', 'image_front_link', 'specialization')


class AuthorSerializer(serializers.ModelSerializer):
    images = ImageSpecializationSerializer(many=True, required=False)
    aliases = serializers.PrimaryKeyRelatedField(many=True, queryset=AuthorAlias.objects.all(), source='authoralias_set')
    author_api_link = serializers.HyperlinkedIdentityField(view_name='author-detail', source='author_id', read_only=True)
    author_front_link = serializers.HyperlinkedIdentityField(view_name='author-detail-front', source='author_id', read_only=True)

    class Meta:
        model = Author
        fields = (
            'id', 'index', 'main_image',
            'name_ru', 'name_en', 'name_other',
            'begin_date', 'end_date',
            'notes', 'images', 'aliases',
            'author_api_link', 'author_front_link',
        )


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'index', 'name_ru', 'name_en',)


class AuthorSpecSerializer(serializers.Serializer):
    specialization = serializers.ChoiceField(choices=AuthorsSpecialization.SPECIALIZATIONS, source='get_specialization_display')
    author = PrimaryKeySerializerField(serializer=AuthorShortSerializer, queryset=Author.objects.all())
    author_api_link = serializers.HyperlinkedIdentityField(view_name='author-detail', source='author', read_only=True)
    author_front_link = serializers.HyperlinkedIdentityField(view_name='author-detail-front', source='author')


class ImageShortSerializer(serializers.ModelSerializer):
    image_api_link = serializers.HyperlinkedIdentityField(view_name='image-detail', source='self', read_only=True)
    image_front_link = serializers.HyperlinkedIdentityField(view_name='image-detail-front', source='self', read_only=True)

    class Meta:
        model = Image
        fields = (
            'name_ru', 'name_en',
            'create_data',
            'image_api_link', 'image_front_link',
        )


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    main_image = ImageURLField()
    images = PrimaryKeySerializerField(serializer=ImageShortSerializer, many=True, queryset=Image.objects.all())
    entity_api_link = serializers.HyperlinkedIdentityField(view_name='entity-detail', source='self', read_only=True)
    entity_front_link = serializers.HyperlinkedIdentityField(view_name='entity-detail-front', source='self', read_only=True)

    class Meta:
        model = Entity
        fields = (
            'id', 'index',
            'name_ru', 'name_en', 'name_other',
            'begin_date', 'end_date',
            'description', 'notes',
            'source', 'source_link',
            'main_image', 'images',
            'entity_api_link', 'entity_front_link',
        )


class EntityShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'index', 'name_ru', 'name_en', 'name_other', 'begin_date', 'end_date',)


class ImageSerializer(serializers.ModelSerializer):
    authors = AuthorSpecSerializer(many=True, style={'base_template': 'list_fieldset.html'})
    entity_api_link = serializers.HyperlinkedIdentityField(view_name='entity-detail', source='entity')
    entity_front_link = serializers.HyperlinkedIdentityField(view_name='entity-detail-front', source='entity')
    entity = PrimaryKeySerializerField(serializer=EntityShortSerializer, queryset=Entity.objects.all())

    class Meta:
        model = Image
        fields = (
            'id',
            'image',
            'name_ru', 'name_en', 'name_other',
            'description', 'description_lat', 'notes',
            'create_data', 'source_link',
            'authors', 'entity', 'entity_api_link', 'entity_front_link',
        )
