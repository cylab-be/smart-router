<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Hosts extends Model
{
    protected $table = 'Hosts';
    protected $fillable = ['mac', 'hostname', 'first_activity'];
}
