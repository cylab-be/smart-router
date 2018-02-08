<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Alerts extends Model
{
    protected $tables = 'Alerts';
    protected $fillable = ['mac', 'hostname', 'domain_reached', 'infraction_date'];
}
