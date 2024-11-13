from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
def home(request):
    return render(request,'ece.html')
def base(request):
    return render(request,'base.html')
def login1(request):
    return render(request,'login.html')
def photo(request):
    return render(request,'photo.html')
def homepage(request):
    return render(request,'homepage.html')

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render
def UserRegisterPageCall(request):
    return render(request, 'UserRegisterPage.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'UserRegisterPage.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'UserRegisterPage.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'homepage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'UserRegisterPage.html')
    else:
        return render(request, 'UserRegister.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('home')  # Redirect to home or another page after login
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Stay on the login page with an error message

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

from .forms import *
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'add_task.html',
                  {'form': form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file, parse_dates=['Date'], dayfirst=True)
        total_sales = df['Sales'].sum()
        average_sales = df['Sales'].mean()

        df['Month'] = df['Date'].dt.month
        monthly_sales = df.groupby('Month')['Sales'].sum()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_sales.index = monthly_sales.index.map(lambda x: month_names[x-1])

        plt.pie(monthly_sales, labels=monthly_sales.index, autopct='%1.1f%%')
        plt.title('Sales Distribution per Month')

        # Process of converting the chart and sending it to the HTML
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return render(request, 'chart.html', {
            'total_sales': total_sales,
            'average_sales': average_sales,
            'chart': image_data
        })
    return render(request, 'chart.html', {'form': UploadFileForm()})