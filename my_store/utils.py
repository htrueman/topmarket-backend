# import requests
# from my_store.models import MyStore, LogoWithPhones, SocialNetwork, DeliveryAndPayment, HowToUse, Contacts, AboutUs
# from django.shortcuts import get_object_or_404
#
# from .serializers import MyStoreInfoHeaderFooterSerializer, \
#     MyStoreSliderImagesSerializer, LogoWithPhonesSerializer, SocialNetworkSerializer, DeliveryAndPaymentSerializer, \
#     HowToUseSerializer, ContactsSerializer, AboutUsSerializer, MyStoreDomainSerializer
#
#
# def send_general_data_to_gen_site_domain(instance_id, request):
#     my_store = get_object_or_404(MyStore, id=instance_id)
#     serializer = MyStoreDomainSerializer(my_store)
#     print(serializer.data)
#
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_header(instance_id, request):
#     my_store = get_object_or_404(MyStore, id=instance_id)
#     serializer = MyStoreInfoHeaderFooterSerializer(my_store)
#     print(serializer.data)
#
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_slider(instance_id, request):
#     my_store = get_object_or_404(MyStore, id=instance_id)
#     serializer = MyStoreSliderImagesSerializer(my_store)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_logo(instance_id, request):
#     logo = get_object_or_404(LogoWithPhones, id=instance_id)
#     serializer = LogoWithPhonesSerializer(logo)
#     print(serializer)
#
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_network(instance_id, request):
#     network = get_object_or_404(SocialNetwork, id=instance_id)
#     serializer = SocialNetworkSerializer(network)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_delivery(instance_id, request):
#     network = get_object_or_404(DeliveryAndPayment, id=instance_id)
#     serializer = DeliveryAndPaymentSerializer(network)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_use(instance_id, request):
#     network = get_object_or_404(HowToUse, id=instance_id)
#     serializer = HowToUseSerializer(network)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_contact(instance_id, request):
#     network = get_object_or_404(Contacts, id=instance_id)
#     serializer = ContactsSerializer(network)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
# def send_general_data_to_gen_site_about_us(instance_id, request):
#     network = get_object_or_404(AboutUs, id=instance_id)
#     serializer = AboutUsSerializer(network)
#     print(serializer)
#     # requests.post(
#     #     data=data
#     # )
#
#
