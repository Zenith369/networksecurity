import os

class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        '''Syncs a local folder to a S3 bucket.'''
        os.system(f"aws s3 sync {folder} {aws_bucket_url}")

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        '''Syncs a folder from s S3 bucket to a local folder.'''
        os.system(f"aws s3 sync {aws_bucket_url} {folder}")