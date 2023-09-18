from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from datetime import datetime
from django.http import JsonResponse
import json
# Create your views here.

def offered_passes(toll_pid):
    return "Toll Pass prices"

class ProcessVehicle(APIView):

    def post(self, request):
        request_serializer = ProcessVehicleRequestSerializer(data = request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        try:
            vehicle = Vehicle.objects.get(registration_num = validated_data['vehicle_num'])
            toll = Toll.objects.get(pid = validated_data['toll_pid'])
            vehicle_passes = vehicle.vehicle_passes
            final_vehicle_passes = []
            for vehicle_pass in vehicle_passes:
                if vehicle_pass.toll_pid == validated_data['toll_pid'] and vehicle_pass.is_valid:
                    final_vehicle_passes.append(vehicle_pass)
            if len(final_vehicle_passes) == 1:
                if final_vehicle_passes[0].pass_type == 'return_pass':
                    final_vehicle_passes[0].is_valid = False
                    VehicleProcessed.objects.create(
                        toll_pid =validated_data['toll_pid'],
                        vehicle_pid = vehicle.pid,
                        charge = 0
                    )
                    toll.vehicles_processed += 1
                    toll.save()
                    return final_vehicle_passes[0]
                else:
                    days_elapsed = datetime.now() - final_vehicle_passes[0].created_on
                    if days_elapsed.days > 7:
                       final_vehicle_passes[0].is_valid = False 
                       return offered_passes(validated_data['toll_pid'])
                    else:
                        VehicleProcessed.objects.create(
                            toll_pid =validated_data['toll_pid'],
                            vehicle_pid = vehicle.pid,
                            charge = 0
                        )
                        toll.vehicles_processed += 1
                        toll.save()
                        return final_vehicle_passes[0]
            else:
                return Response(offered_passes(validated_data['toll_pid']), status = status.HTTP_200_OK)
                
        except Exception as e:
            return Response("Error encountered", status=status.HTTP_400_BAD_REQUEST)

class LeaderBoard(APIView):

    def get(self, request):
        tolls = Toll.objects.all()
        vehicles_processed = []
        charges_collected = []
        for toll in tolls:
            vehicles_processed.append([toll.vehicles_processed, toll.pid])
            charges_collected.append([toll.charges_collected, toll.pid])
        vehicles_processed.sort()
        charges_collected.sort()
        response = {"vehicles_processed":vehicles_processed, "charges_collected":charges_collected}
        return JsonResponse(response)
