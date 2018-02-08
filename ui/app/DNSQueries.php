<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class DNSQueries extends Model
{
    protected $table = 'DNSQueries';
    protected $fillable = ['ip', 'domain', 'datetime'];
}
