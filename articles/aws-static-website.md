[godaddy-dns]: aws-static-website-images/godaddy-dns.png
[s3-public-access]: aws-static-website-images/s3-public-access.png
[s3-static-website-hosting]: aws-static-website-images/s3-static-website-hosting.png
[s3-buckets]: aws-static-website-images/s3-buckets.png
[s3-redirect-requests]: aws-static-website-images/s3-redirect-requests.png

# Lightning fast website using AWS

## Motivation
If you follow this article along, at the end you should end up with lightning fast website just like this one.

## Implementation
We'll be using:

- [S3](https://docs.aws.amazon.com/s3/index.html) for storing our documents
- [Cloudfront](https://docs.aws.amazon.com/cloudfront/index.html) for content distribution
- [Route 53](https://docs.aws.amazon.com/route53/index.html) for DNS management
- [Lambda@Edge](https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html) with Javascript for routing
- [Lambda](https://docs.aws.amazon.com/lambda/index.html) with Python to generate html files from markdown
- [ACM](https://docs.aws.amazon.com/acm/index.html) for certificates

> All region-based services from this tutorial must located in *US-east (N. Virginia)*. It's because some services, like Lambda@Edge are not available in other regions. We will use global CDN so it doesn't matter where are the services really located.

### Domain Name
First you'll need a domain for your new website. You can use your favorite registrar, it doesn't have to be AWS. I manage all my domains with GoDaddy and want it to stay that way. But it order to use my domain with Cloudfront, I have to use AWS name servers and manage the DNS records there.

For that we'll use Route 53. Create new public Hosted Zone for your domain. After you do so, you'll get list of name servers you need to set up for your domain.

```
ns-729.awsdns-27.net
ns-61.awsdns-07.com
ns-1266.awsdns-30.org
ns-2011.awsdns-59.co.uk
```

![Godaddy NS setting][godaddy-dns]

> If you, like me, already have some DNS records setup, write them down before you change the NS servers because the'll get removed in the process. I already used my domain for email so I had to move my MX records to AWS.

We'll return to Route 53 later when we'll use it to setup DNS.

### S3
All our documents will be stored in S3. We need to create 2 buckets - one for for url with www ([https://www.tesarek.me](www.tesarek.me)) and on without it ([https://tesarek.me](tesarek.me)). Decide which version will be primary, the other one will redirect to it. I don't like the www in from of my urls so [https://tesarek.me](tesarek.me) is my primary.

![S3 Buckets][s3-buckets]

When creating the buckets name them exactly like your domain - `domain.com` and `www.domain.com` and don't forget to create them in US-east (N. Virginia).

> S3 bucket names must be globally unique and deleting them takes few hours. If you create you bucket in wring region and then you remove it, it will take few hours until AWS will allow to create new bucket with the same name.

Now we need to configure our buckets. In Properties tab, click on Static Website hosting. For your primary bucket, choose *Use this bucket to host a website* and in fill in `index.html` as your index document.

![S3 Static Website Hosting][s3-static-website-hosting]

For the secondary bucket choose *Redirect requests* and put the name of your primary bucket into *Target bucket or domain*.

![S3 redirect requests][s3-redirect-requests]

Thanks to this settings you only have to store your documents in only one bucekt and requests to the secondary bucket will be redirected to the primary one.

Before testing it works we need to set the permissions to everyone to read our documents. For both buckets click open Permissions tab and allow Public access to List objects.

![S3 Public list access][s3-public-access]

Now everyone can list content of our buckets but still can't read our pages. Permissions to documents are set on individual documents. You can do that manually every time you create new document. I prefer not to do that so I set up a bucket policy that set's the permissions for me by default.

For your main bucket, click Permissions and then Bucket Policy. Copy this JSON into the bucket policy editor:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::tesarek.me/*"
        }
    ]
}
```

Don't forget to change the bucket name in resource ARN.

> The Version is version of the Policy JSON format, not the version of your policy. Don't change it.

Now we are done with S3. To test everything works correctly upload index.html with some content into the primary bucket. When you click on the file in AWS console, you'll get, among other things, the url of the file, something like [https://s3.amazonaws.com/tesarek.me/index.html](https://s3.amazonaws.com/tesarek.me/index.html) This url should show the html file you just uploaded. Try also the secondary bucket url but adding/removing www: [https://s3.amazonaws.com/www.tesarek.me/index.html](https://s3.amazonaws.com/www.tesarek.me/index.html).


### Certificate
We'll use Amazon Certificate Service to request our SSL certificate. The process is quite simple, in ACS console click on *Request Certificate*, leave *Request public certificate* selected and confirm. Attach both your second level and third level domains to the certificate and confirm.

After you confirm ownership of the domains with your prefered method, you'll be able to use the certificate.

### CloudFront & CDN
CloudFront is a service that we'll put in front of our S3 buckets and it will do SSL resolution and also work as CDN.We can also filter all incoming requests through Lambda@Edge and thus implement routing.

Start by creating new web Cloudfront distribution.

Fill in your primary bucket as Origin Domain Name and leave default values everywhere else.

In Cache setting, select *Redirect HTTP to HTTPS*. You may also disable cache for some time by setting all TTLs to 0. It makes debugging easier. You can turn chaching on, when you're done.

In distribution setting fill in both your domains and also select the certificate from previous step.


