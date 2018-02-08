<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class HTTPQueries extends Model
{
    protected $table = 'HTTPQueries';
    protected $fillable = ['mac_iot', 'domain', 'datetime'];
}
