from rest_framework.response import Response
from rest_framework import status

from datetime import datetime


def validate_datetime(func):
    def search(view, request, *args, **kwargs):
        try:
            data = request.data
            if data.get('date_param') is not None:
                kwargs['param'] = {
                    'type': 'date',
                    'data': datetime.strptime(data.get('date_param'), '%Y-%m-%d')
                }
            elif data.get('datetime_param') is not None:
                kwargs['param'] = {
                    "type": "datetime",
                    "data": datetime.strptime(data.get('datetime_param'), '%Y-%m-%d %H:%M:%S')
                }
            else:
                return Response({"error": "Please provide either date_param or datetime_param for searching"}, status=status.HTTP_400_BAD_REQUEST)
            return func(view, request, *args, **kwargs)
        except Exception as e:
            return Response({"error": "Invalid datetime format"}, status=status.HTTP_400_BAD_REQUEST)
    return search