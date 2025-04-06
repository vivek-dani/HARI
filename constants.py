from os.path import join

#unique_id="eeb25f32-91f4-4384-bd63-9efaefc2a228"
unique_id="294086b1-d4dd-4e64-bfe0-88492f561d65"
bucket = "rabbit-bucket-vivek"
profile_name = "rabbit-hole-participant"
region='ap-south-1'
collection_id = "vivek-face-collection"
aws_access_key_id="", 
aws_secret_access_key=""
base_dir="C:\\Users\\Admin\\Documents\\inference"
train_base_dir=join("C:\\Users\\Admin\\Documents",unique_id)
rag_path=join(train_base_dir, "rag")
video_path="C:\\Users\\Admin\\Documents\\video"
action_items_file = join(train_base_dir, "actions.jsonl")