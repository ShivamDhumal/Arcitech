from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, contentserializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, content_item, category
from django.db.models import Q

@api_view(['POST'])
def register_user(request):
    """
    Register a new user.

    Args:
        request (Request): The request object containing user registration data.

    Returns:
        Response: A response indicating the success or failure of the registration.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Registration successfully done'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    """
    Authenticate a user and return an authentication token.

    Args:
        request (Request): The request object containing login credentials.

    Returns:
        Response: A response containing the authentication token or an error message.
    """
    if request.method == 'POST':
        print("enter in login")
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Log out the authenticated user by deleting their token.

    Args:
        request (Request): The request object.

    Returns:
        Response: A response indicating the success or failure of the logout.
    """
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_content(request):
    """
    Create a new content item.

    Args:
        request (Request): The request object containing content data.

    Returns:
        Response: A response indicating the success or failure of the content creation.
    """
    if request.method == "POST":
        serializer = contentserializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'success': 'Content added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def content_data(request, id=None):
    """
    Retrieve, update, or delete a content item based on the request method and user's permissions.

    Args:
        request (Request): The request object.
        id (int, optional): The ID of the content item. Defaults to None.

    Returns:
        Response: A response containing the content data, success message, or an error message.
    """
    try:
        if id:
            if request.user.is_superuser:
                content = content_item.objects.get(id=id)
            else:
                try:
                    content = content_item.objects.get(id=id, user=request.user)
                except content_item.DoesNotExist:
                    return Response({'error': 'Access denied. You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

            if request.method == 'GET':
                serializer = contentserializer(content)
                return Response(serializer.data)
            elif request.method == 'PUT':
                serializer = contentserializer(content, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Content updated successfully'})
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                content.delete()
                return Response({'message': 'Content deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            if request.user.is_superuser:
                content = content_item.objects.all()
            else:
                content = content_item.objects.filter(user=request.user)

            serializer = contentserializer(content, many=True)
            return Response(serializer.data)

    except content_item.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_content(request):
    """
    Search for content items based on a query parameter.

    Args:
        request (Request): The request object containing search parameters.

    Returns:
        Response: A response containing the search results.
    """
    if request.method == 'GET':
        search_query = request.query_params.get('search', '')

        try:
            content = content_item.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

            serializer = contentserializer(content, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
