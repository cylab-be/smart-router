<!doctype html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Smart-router</title>

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css?family=Raleway:100,600" rel="stylesheet" type="text/css">

    <!-- Styles -->
    <style>
        html, body {
            background-color: #fff;
            color: #636b6f;
            font-family: 'Raleway', sans-serif;
            font-weight: 100;
            height: 100vh;
            margin: 0;
        }

        .full-height {
            height: 100vh;
        }

        .flex-center {
            align-items: center;
            display: flex;
            justify-content: center;
        }

        .position-ref {
            position: relative;
        }

        .top-right {
            position: absolute;
            right: 10px;
            top: 18px;
        }

        .content {
            text-align: center;
        }

        .title {
            font-size: 84px;
        }

        .links > a {
            color: #636b6f;
            padding: 0 25px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: .1rem;
            text-decoration: none;
            text-transform: uppercase;
        }

        .m-b-md {
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
<div class="flex-center position-ref full-height">
    @if (Route::has('login'))
        <div class="top-right links">
            @auth
                <a href="{{ url('/home') }}">Home</a>
                @else
                    <a href="{{ route('login') }}">Login</a>
                    <a href="{{ route('register') }}">Register</a>
                    @endauth
        </div>
    @endif

    <div class="content">
        <div class="title m-b-md">
            Smart-router
        </div>
        <h3>HTTP Traffic</h3>
        @php($HTTPQueries = DB::select('select * from HTTPQueries '))
        <table style="width:100%">
            <tr>
                <th>ip iot</th>
                <th>Domain</th>
                <th>Date </th>
            </tr>

            @foreach($HTTPQueries as $query)
            <tr>
                <td>{{$query->ip_iot}}</td>
                <td>{{$query->domain}}</td>
                <td>{{$query->datetime}}</td>
            </tr>
            @endforeach

        </table>


        <h3>DNS Traffic</h3>
        @php($DNSQueries = DB::select('select * from DNSQueries '))
        <table style="width:100%">
            <tr>
                <th>ip iot</th>
                <th>ip dst</th>
                <th>Domain</th>
                <th>Date </th>
            </tr>

            @foreach($DNSQueries as $query)
                <tr>
                    <td>{{$query->ip_iot}}</td>
                    <td>{{$query->ip_dst}}</td>
                    <td>{{$query->domain}}</td>
                    <td>{{$query->datetime}}</td>
                </tr>
            @endforeach

        </table>



    </div>
</div>
</body>
</html>
