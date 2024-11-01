import json
import requests
from django.shortcuts import render, get_object_or_404  
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Account, Destination

URLS = ['http://127.0.0.1:8000/get-create-accounts', 'http://127.0.0.1:8000/get-delete-account']

# Create your views here.
@csrf_exempt
def account_get_post(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        response_data = [{"id": account.id, "email": account.email, "account_id": account.account_id, "account_name": account.account_name, "app_secret_token": account.app_secret_token, "website": account.website} for account in accounts]
        return JsonResponse(response_data, safe = False)

    elif request.method == 'POST':
        request_data = json.loads(request.body)
        email = request_data.get('email')
        account_name = request_data.get('account_name')
        website = request_data.get('website')

        if email == None or account_name == None:
            response_data = {'message': 'Please provide all mandatory fields.'}
        else:
            account = Account.objects.create(
                email = email,
                account_name = account_name,
                website = website
            )
            response_data = {
                "id": account.id,
                "email": account.email,
                "account_id": str(account.account_id),
                "account_name": account.account_name,
                "app_secret_token": account.app_secret_token,
                "website": account.website,
            }

            return JsonResponse(response_data)


@csrf_exempt
def account_get_delete(request, account_id):
    account = Account.objects.filter(id = account_id).first()
    response_data = {}

    if account:
        if request.method == 'GET':
            response_data = {
                'id': account.id,
                'email': account.email,
                'account_id': account.account_id,
                'account_name': account.account_name,
                'app_secret_token': account.app_secret_token,
                'website': account.website,
            }
            return JsonResponse(response_data)

        elif request.method == 'DELETE':
            account.delete()
            response_data = {'message': 'Account deleted successfully.'}
            return JsonResponse(response_data)

        elif request.method == 'PUT':
            request_data = json.loads(request.body)
            account_id = request_data.get('account_id')
            
            account = Account.objects.filter(id = account_id).first()

            if account:
                email = request_data.get('email') if request_data.get('email') else account.email
                account_name = request_data.get('account_name') if request_data.get('account_name') else account.account_name
                website = request_data.get('website') if request_data.get('website') else account.website 

                Account.objects.filter(id = account_id).update(email = email, account_name = account_name, website = website)
                response_data = {'message': 'Account updated successfully.'}
                return JsonResponse(response_data)
            
            else:
                response_data = {'message': 'No account found.'}
                return JsonResponse(response_data)

    else:
        response_data = {'message': 'No account found.'}
        return JsonResponse(response_data)


@csrf_exempt
def destination_get_post(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        response_data = [{'id': destination.id, 'account_id': str(destination.account.account_id), 'url': destination.url, 'http_method': destination.http_method, 'headers': destination.headers} for destination in destinations]
        return JsonResponse(response_data, safe = False)
    
    elif request.method == 'POST':
        request_data = json.loads(request.body)
        print(request_data)
        account_id = request_data.get('account_id')
        url = request_data.get('url')
        http_method = request_data.get('http_method')
        headers = request_data.get('headers')

        if url == None or http_method == None or headers == None:
            response_data = {'message': 'Please provide all mandatory fields.'}
            return JsonResponse(response_data)

        else:
            account_id = Account.objects.filter(account_id = account_id).first().id

            if account_id:
                if url in URLS:
                    destination = Destination.objects.create(
                        account_id = account_id,
                        url = url,
                        http_method = http_method,
                        headers = headers,
                    )

                    response_data = {
                        'id': destination.id,
                        'account_id': destination.account_id,
                        'url': destination.url,
                        'http_method': destination.http_method,
                        'headers': destination.headers,
                    }

                    return JsonResponse(response_data)
                else:
                    response_data = {'message': 'Please provide a valid URL.', 'Valid URLs': URLS}
        
            else:
                response_data = {'message': 'No account with the given account_id found.'}


@csrf_exempt
def destination_get_delete(request, destination_id):
    destination = Destination.objects.filter(id = destination_id).first()
    response_data = {}

    if destination:
        if request.method == 'GET':
            response_data = {
                'id': destination.id,
                'account_id': str(destination.account.account_id),
                'url': destination.url,
                'http_method': destination.http_method,
                'headers': destination.headers,
            }

            return JsonResponse(response_data)

        elif request.method == 'DELETE':
            destination.delete()
            response_data = {'message': 'Destination deleted successfully.'}
            return JsonResponse(response_data)

        elif request.method == 'PUT':
            request_data = json.loads(request.body)
            destination_id = request_data.get('destination_id')
            
            destination = Destination.objects.filter(id = destination_id).first()

            if destination:
                url = request_data.get('url')
                http_method = request_data.get('http_method') if request_data.get('http_method') else destination.http_method
                headers = request_data.get('headers') if request_data.get('headers') else destination.headers
                print(headers)
                account = request_data.get('account_id')

                if account:
                    account_id = Account.objects.filter(account_id = account).first().id
                else:
                    account_id = destination.account.id
                

                if url:
                    if url in URLS:
                        url = url
                    else:
                        response_data = {'message': 'Please provide a valid URL', 'Valid URLs': URLS}
                        return JsonResponse(response_data)
                else:
                    url = destination.url

                Destination.objects.filter(id = destination_id).update(url = url, http_method = http_method, headers = headers, account_id = account_id)
                response_data = {'message': 'Destination updated successfully.'}
                return JsonResponse(response_data)                    
                
            else:
                response_data = {'message': 'No destination found.'}
                return JsonResponse(response_data)


        else:
            response_data = {'message': 'No destination found.'}
            return JsonResponse(response_data)


def destination_get_account(request, account_id):
    response_data = {}
    account_id = Account.objects.filter(account_id = account_id).first().id

    if account_id:
        destinations = Destination.objects.filter(account_id = account_id)
        if destinations:
            response_data = [{'account_id': destination.account.account_id, 'url': destination.url} for destination in destinations]
            return JsonResponse(response_data, safe = False)
        else:
            response_data = {'message': 'No destination URLs found for the account'}
    else:
        response_data = {'message': 'No account found.'}


def handle_data(request):
    response_data = {}

    if request.method == 'GET':
        if request.content_type == 'application/json':
            header_token = request.headers.get('CL-X-TOKEN')
            if header_token:
                account_id = Account.objects.filter(app_secret_token = header_token).first().id
                if account_id:
                    destinations = Destination.objects.filter(account_id = account_id)
                    if destinations:
                        for destination in destinations:
                            headers = destination.headers   
                            if destination.http_method == 'PUT':
                                data = json.loads(request.body)
                                data['account_id'] = account_id
                                request_data = json.dumps(data)
                                url = f"{destination.url}/{account_id}"
                                response = requests.put(url, data = request_data, headers = headers)
                                response_data[destination.url] = response.json()
                            elif destination.http_method == 'GET':
                                if destination.url == 'http://127.0.0.1:8000/get-create-accounts':
                                    url = destination.url
                                else:
                                    url = f"{destination.url}/{account_id}"
                                response = requests.get(url, headers = headers)
                                response_data[destination.url] = response.json()
                        return JsonResponse(response_data, safe = False)
                    else:
                        response_data = {'message': 'No destination found.'}  
                        return JsonResponse(response_data)  

                else:
                    response_data = {'message': 'No account found.'}
                    return JsonResponse(response_data)


            else:
                response_data = {'message': 'Un Authenticate'}
                return JsonResponse(response_data)


        else:
            response_data = {'message': 'Invalid Data'}
            return JsonResponse(response_data)

        pass

    pass





