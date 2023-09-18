from rest_framework import serializers

class ProcessVehicleRequestSerializer(serializers.Serializer):
    vehicle_num = serializers.CharField()
    toll_pid = serializers.CharField()
