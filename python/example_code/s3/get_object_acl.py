# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


import boto3


def get_object_acl(bucket_name, object_name):
    """Retrieve the access control list of an Amazon S3 bucket object.

    :param bucket_name: string
    :param object_name: string
    :return: Object access control list of grantees and permissions. If error, return None.
    """

    s3 = boto3.client('s3')
    try:
        response = s3.get_object_acl(Bucket=bucket_name, Key=object_name)
    except Exception as err:
        # err.response['Error']['Code'] == 'NoSuchKey', etc.
        return None
    return response['Grants']


def main():
    test_bucket_name = 'test-bucket-name'
    test_object_name = 'test-object-name'
    acl = get_object_acl(test_bucket_name, test_object_name)

    if acl is None:
        print('ERROR: Could not retrieve object ACL')
    else:
        # Output the object ACL grantees and permissions
        for grantee in acl:
            # The grantee type determines the grantee_identifier
            grantee_type = grantee['Grantee']['Type']
            if grantee_type == 'CanonicalUser':
                grantee_identifier = grantee['Grantee']['DisplayName']
            elif grantee_type == 'AmazonCustomerByEmail':
                grantee_identifier = grantee['Grantee']['EmailAddress']
            elif grantee_type == 'Group':
                grantee_identifier = grantee['Grantee']['URI']
            else:
                grantee_identifier = 'Unknown'
            print('Grantee: {0}, Permissions: {1}'.format(grantee_identifier, grantee['Permission']))


if __name__ == '__main__':
    main()

# snippet-comment:[These are tags for the AWS doc team's sample catalog. Do not remove.]
# snippet-sourcedescription:[get_object_acl.py demonstrates how to retrieve the access control list of an Amazon S3 bucket object.]
# snippet-keyword:[Python]
# snippet-keyword:[AWS SDK for Python (Boto3)]
# snippet-keyword:[Code Sample]
# snippet-keyword:[Amazon S3]
# snippet-service:[s3]
# snippet-sourcetype:[full-example]
# snippet-sourcedate:[2018-11-08]
# snippet-sourceauthor:[scalwas (AWS)]
