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
        @php($HTTPQueries = DB::select('select * from HTTPQueries Order by datetime'))
        <table style="width:100%">
            <tr>
                <th>Mac iot</th>
                <th>Domain</th>
                <th>Date </th>
            </tr>

            @foreach($HTTPQueries as $query)
            <tr>
                <td>{{$query->mac_iot}}</td>
                <td>{{$query->domain}}</td>
                <td>{{$query->datetime}}</td>
            </tr>
            @endforeach

        </table>


        <h3>DNS Traffic</h3>
        @php($DNSQueries = DB::select('select * from DNSQueries order by datetime'))
        <table style="width:100%">
            <tr>
                <th>ip dst</th>
                <th>Domain</th>
                <th>Date </th>
            </tr>

            @foreach($DNSQueries as $query)
                <tr>
                    <td>{{$query->ip}}</td>
                    <td>{{$query->domain}}</td>
                    <td>{{$query->datetime}}</td>
                </tr>
            @endforeach

        </table>

        <h3>Hosts</h3>
        @php($Hosts = DB::select('select * from Hosts order by first_activity'))
        <table style="width:100%">
            <tr>
                <th>MAC</th>
                <th>Hostname</th>
                <th>First Activity Detected</th>
            </tr>

            @foreach($Hosts as $host)
                <tr>
                    <td>{{$host->mac}}</td>
                    <td>{{$host->hostname}}</td>
                    <td>{{$host->first_activity}}</td>
                </tr>
            @endforeach

        </table>

        <h3>Alerts</h3>
        @php($Alerts = DB::select('select * from Alerts order by infraction_date'))
        <table style="width:100%">
            <tr>
                <th>MAC</th>
                <th>Hostname</th>
                <th>Domain Reached</th>
                <th>@</th>
            </tr>

            @foreach($Alerts as $alert)
                <tr>
                    <td>{{$alert->mac}}</td>
                    <td>{{$alert->hostname}}</td>
                    <td>{{$alert->domain_reached}}</td>
                    <td>{{$alert->infraction_date}}</td>
                </tr>
            @endforeach

        </table>



    </div>
</div>
</body>
</html>
