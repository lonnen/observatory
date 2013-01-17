# Observatory

Observatory is a flask app that observes and centralizes information about
Socorro development and deployment inside Mozilla.

## API Description

### Get all releases

```
GET /releases
```

Answers with a JSON object containing an array of all releases, including those in-progress and under active development

#### Example response
```
{
    "releases": {
        {
            message: "unreleased",
            tag: "v35",
            ref: "refs/tags/v35"
        },
        ...
        {
            "url": "https://api.github.com/repos/mozilla/socorro/git/refs/tags/v33",
            "object": {
                "url": "https://api.github.com/repos/mozilla/socorro/git/tags/42a90b33f43d8ea8509821b54ba922d5903e9d3b",
                "sha": "42a90b33f43d8ea8509821b54ba922d5903e9d3b",
                "type": "tag"
            },
            "ref": "refs/tags/v33"
        },
        ...
}
```

### Get a specific release
```
GET /release/<release>
```
```
GET /releases/v33
```
```
GET /releases/33
```

Answers with a JSON object containing information about a particular release

#### Example responses
```
{
    "sha": "42a90b33f43d8ea8509821b54ba922d5903e9d3b",
    "tag": "v33",
    "tagger": {
        "date": "2013-01-10T23:44:49Z",
        "email": "chris.lonnen@gmail.com",
        "name": "Lonnen"
    },
    "url": "https://api.github.com/repos/mozilla/socorro/git/tags/42a90b33f43d8ea8509821b54ba922d5903e9d3b",
    "message": "bug 829341 - push Socorro 33 release (srsly this time)\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.11 (Darwin)\n\niQIcBAABAgAGBQJQ71KKAAoJEGWUlfXT82vPAC8P/0qkbHp+sPedN22XRHGWpVJT\nVWa4w/WlChh8Qgf2DfzKc8uQeHw0EmSRLiQK5YSA/xOGdekYHX/vlIN4Shm3/Sfm\nIx163NAXrv4HUWxL1Q1YI4bfRi/3SeGt74RrF0+mYe+kTsh1VeJFH4x0xv/pnQWz\nVmCWpBFxSXjMKGwjZTn4RCu12aBlv51nOT3/j6tdVJ1odVzl+BAtvt6sr1RiAldn\nMiD+kfHT6CGi6Fo6SkMRfhovrf1NMCjMZs30F+KxHPHFpD0ZzVHe8CtURdyELQBr\nocO8ki1Nvj6/GRQURcC8NGxuN62aw1FV5DChiTW/6A6iH/wmkIHm7emjmKeWow+o\n2Wur58NFjZ+4e0VNBpfArL3J0U1J93O1C1Ukq2r8dZ/mF5ym44UQRpf01I2W1dhN\nynFILNakfEs3czDyKT6mbOjVbFemmmX/yv8vQcc20EHyBKfgu4XM6TSDEyY2V9Lt\nJbhDr3fDN5DvSGC09e0itgM94N018r8skqGrlyFrEFUWoptq8/R1RmM5PLGfXgA0\n1hJjyb8CxBNRgRCPCplYmqmvOuZRQ+lEKAzMQAyZHOfYIvrwFzdzRjf+knK1Z1nJ\ne4t+8HQzMOWS7/mIIXlHkJA/DxYS91awRq9+h6fdv5qy7oN4AGwQq/JOZeMOKblW\nxKq+y+QNcNB9Z1qP1DM1\n=8XzO\n-----END PGP SIGNATURE-----\n",
    "object": {
        "url": "https://api.github.com/repos/mozilla/socorro/git/commits/1496281f8da7a13c8883961a7a235719383533f5",
        "sha": "1496281f8da7a13c8883961a7a235719383533f5",
        "type": "commit"
    }
}
```

### Get all environments

```
GET environments/
```

Answers a list of known deployments and what versions are deployed there.

#### Example response
```
{
    "prod": {
        "socorroRevision": "1496281f8da7a13c8883961a7a235719383533f5",
        "data": [ … ],
        "plotData": { … },
        "breakpadRevision": "1094"
    },
    "dev": {
        "socorroRevision": "21a8fbae8d556b479bd54971800aaf6fa6a43c0c",
        "data": [ … ],
        "plotData": { … },
        "breakpadRevision": "1095"
    },
    "stage": {
        "socorroRevision": "ec6bdf4697187f9ba8db188dc0a95cb71786bfc2",
        "data": [ … ],
        "plotData": { … },
        "breakpadRevision": "1095"
    }
}
```

### Get an environment

```
GET environment/<name>
```
```
GET environment/prod
```

Answers an object with specific information about a deployment.

#### Example response
```
{
    "prod": {
        "breakpadRevision": "1094",
        "data": [
            {
                "date_oldest_job_queued": "Jan 13 2013 23:44:55",
                "date_recently_completed": "Jan 13 2013 23:45:01",
                "processors_count": 10,
                "avg_wait_sec": 4.97584,
                "waiting_job_count": 20,
                "date_created": "Jan 13 2013 23:45:02",
                "id": 441488,
                "avg_process_sec": 2.29823
            },
            ... 
        ],
        "plotData": { 
            waiting_job_count: [ [11, 20], [10, 18] ... ],
            avg_wait_sec: [ [11, 4.97584], [ 10, 5.15729 ], ... ],
            processors_count: [ [11, 10], [10, 9], ... ],
            xaxis_ticks: [ [11, "23:45"], [10, "23:40"], ... ],
            avg_process_sec: [ [11, 2.29823], [10, 2.32124] ... ]
        },
        "socorroRevision": "1496281f8da7a13c8883961a7a235719383533f5"
    }
}
```