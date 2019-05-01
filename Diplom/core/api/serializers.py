from collections import OrderedDict
from rest_framework import serializers

from ..models import Image, Author, Entity, AuthorsSpecialization, Occupation, Land


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
        else:
            return ""


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'


class ImageSpecializationSerializer(serializers.ModelSerializer):
    image_id = serializers.SlugRelatedField(
        read_only=True,
        source='image',
        slug_field='id',
    )
    image_ru = serializers.SlugRelatedField(
        read_only=True,
        source='image',
        slug_field='name_ru',
    )
    image_en = serializers.SlugRelatedField(
        read_only=True,
        source='image',
        slug_field='name_en',
    )
    specialization = serializers.ChoiceField(
        choices=AuthorsSpecialization.SPECIALIZATIONS,
        source='get_specialization_display',
    )

    class Meta:
        model = AuthorsSpecialization
        fields = ('image_id', 'image_ru', 'image_en', 'specialization')


class AuthorSerializer(serializers.ModelSerializer):
    images = ImageSpecializationSerializer(
        many=True,
        required=False,
    )
    occupations = OccupationSerializer(
        many=True,
        required=False,
    )
    lands = LandSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Author
        fields = (
            'id', 'name_ru', 'name_en',
            'begin_date', 'end_date', 'begin_work_date', 'end_work_date',
            'index', 'gnd', 'notes',
            'images', 'occupations', 'lands',
        )


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'index', 'name_ru', 'name_en',)


class AuthorSpecSerializer(serializers.ModelSerializer):
    specialization = serializers.ChoiceField(
        choices=AuthorsSpecialization.SPECIALIZATIONS,
        source='get_specialization_display',
    )
    author = PrimaryKeySerializerField(
        serializer=AuthorShortSerializer,
        queryset=Author.objects.all(),
    )

    class Meta:
        model = AuthorsSpecialization
        fields = ('id', 'author', 'specialization')


class ImageShortSerializer(serializers.ModelSerializer):
    image_front_link = serializers.HyperlinkedIdentityField(
        view_name='image-detail-front',
        source='self',
        read_only=True,
    )

    class Meta:
        model = Image
        fields = (
            'id', 'name_ru', 'name_en',
            'create_date',
            'image_front_link',
        )


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    main_image = ImageURLField()
    images = PrimaryKeySerializerField(
        serializer=ImageShortSerializer,
        many=True,
        queryset=Image.objects.all(),
    )

    class Meta:
        model = Entity
        fields = (
            'id', 'index', 'normdate',
            'name_ru', 'name_en',
            'begin_date', 'end_date',
            'description', 'notes',
            'source', 'source_link',
            'main_image', 'images',
        )


class EntityShortSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'index', 'name_ru', 'name_en', 'begin_date', 'end_date',)


class ImageSerializer(serializers.ModelSerializer):
    authors = AuthorSpecSerializer(
        many=True,
        style={'base_template': 'list_fieldset.html'},
    )
    entity = PrimaryKeySerializerField(
        serializer=EntityShortSerializer,
        queryset=Entity.objects.all(),
    )

    class Meta:
        model = Image
        fields = (
            'id', 'index_image_mu', 'index_image_hab',
            'image', 'thumb_image', 'size',
            'name_ru', 'name_en',
            'description', 'description_lat', 'notes',
            'create_date', 'source_link', 'doublet_links', 'catalog_links',
            'authors', 'entity', 'technique',
        )
