# omni-slo-generator

All in one solution for calculating SLOs. Built on top of 
[google/slo-generator](https://github.com/google/slo-generator).

## How it works

1. Looks through a GCS bucket and finds all SLO manifests ([example](https://github.com/google/slo-generator/blob/master/samples/cloud_monitoring/slo_gae_app_availability.yaml))
2. Calculates the SLOs according to [shared configuration](https://github.com/google/slo-generator/blob/master/samples/config.yaml)
3. Exposes calculated prometheus metrics
4. Sleeps for a given interval

## Assumptions

Feel free to create a Pull Request that allows for more setups, as it is
this project is meant to work in a very specific way:

* Made to run in GKE
* SLO manifests are stored in GCS bucket

## What is it missing

Alerts still need to be created 'manually'. It's hard to have one way of alerting.

## Why

Before this, we at Heureka Group ran slo-generator in API mode with a cronjob
listing the bucket and pushing it to the API. This caused a number of issues.
This solution should be way more efficient.

## Developing

It's not out of the box ready. Because as everything, this is being put together
in a bit of a rush.

1. In docker-compose
   1. Replace `OMNI_SLO_GENERATOR_SLO_GCS_BUCKET` with a bucket you want to test against
   2. Add SA credentials with permissions for that bucket into `sample/credentials.json`
   3. Adjust your desired backends in `sample/config.yaml`
