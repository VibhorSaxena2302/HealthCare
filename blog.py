from db_setup import BlogPost, Comment, SessionLocal
import streamlit as st
from google.cloud import storage
import os
import tempfile
from PIL import Image
import utility

def setup_gcs_credentials(json_key_path):
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key_path
    print(f"Environment variable set for credentials: {json_key_path}")
    
# Google Cloud Storage upload function
def upload_to_gcs(image_file, bucket_name, blob_name):
    json_key_path = r"C:\Users\shrey\Git Uploads\HealthCare\LLM\google_cloud_api\storage-441514-c40e275bbda9.json"
    setup_gcs_credentials(json_key_path)

    """Uploads a file to Google Cloud Storage and returns the public URL."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Upload image
    blob.upload_from_filename(image_file)
    
    return blob.public_url

# Function to download the image from GCS to a temp directory
def download_image_from_gcs(image_url, temp_dir, max_width=300, max_height=300):
    json_key_path = "/Users/vibhor/Documents/Projects/gfg_hackathon/LLM/google_cloud_api/uchat-431212-d06dd3414788.json"
    setup_gcs_credentials(json_key_path)
    """Download the image from GCS and save it to a temp directory."""
    storage_client = storage.Client()
    
    # Extract bucket and blob info from the URL
    url_parts = image_url.replace("https://storage.googleapis.com/", "").split("/", 1)
    bucket_name = url_parts[0]
    blob_name = url_parts[1]
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Create a temporary file path
    local_image_path = os.path.join(temp_dir, blob_name.split("/")[-1])
    
    # Download the image to the temp directory
    blob.download_to_filename(local_image_path)
    
    # Open and resize the image using Pillow
    with Image.open(local_image_path) as img:
        # Resize the image while maintaining aspect ratio
        img.thumbnail((max_width, max_height))
        resized_image_path = os.path.join(temp_dir, f"resized_{blob_name.split('/')[-1]}")
        img.save(resized_image_path)
    
    return resized_image_path

def create_blog():
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.subheader("Create New Blog Post")
        title = st.text_input("Title")
        description = st.text_area("Description")
        content = st.text_area("Content")
        
        # Image upload section
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if st.button("Post"):
            image_url = None
            if uploaded_image:
                # Save image temporarily
                temp_dir = tempfile.mkdtemp()
                image_path = os.path.join(temp_dir, uploaded_image.name)
                
                # Save the image file locally 
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                # Upload image to GCS
                bucket_name = "gfgstorage0"
                blob_name = f"blog_images/{uploaded_image.name}"
                image_url = upload_to_gcs(image_path, bucket_name, blob_name)
                
                st.success(f"Image uploaded successfully: {image_url}")

                utility.rm_directory(temp_dir)

            # Create and save the blog post
            with SessionLocal() as db:
                blog_post = BlogPost(
                    title=title,
                    description=description,
                    content=content,
                    author_id=st.session_state['user_id'],
                    likes=0,
                    image_url=image_url  # Store the image URL
                )
                db.add(blog_post)
                db.commit()
                st.success("Blog post created successfully!")
    else:
        st.warning("Please log in to create a blog post.")

def like_post(post_id):
    with SessionLocal() as db:
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        post.likes += 1
        db.commit()

def view_blogs():
    st.subheader("Blog Posts")

    if 'page' not in st.session_state:
        st.session_state['page'] = 0

    per_page = 10
    current_page = st.session_state['page']

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    with SessionLocal() as db:
        total_posts = db.query(BlogPost).count()
        total_pages = total_posts // per_page

        posts = db.query(BlogPost).offset(current_page * per_page).limit(per_page).all()

        for post in posts:
            st.write(f"### {post.title} (Posted by: {post.author.username})")
            st.write(post.description)
            st.write(post.content)

            # If an image URL is available, download and display the image
            if post.image_url:
                try:
                    local_image_path = download_image_from_gcs(post.image_url, temp_dir)
                    st.image(local_image_path, caption="Uploaded Image", use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying image: {e}")

            st.write(f"**Likes:** {post.likes}")

            # Like button
            if st.button(f"Like", key=f"like_{post.id}"):
                if 'logged_in' in st.session_state and st.session_state['logged_in']:
                    like_post(post.id)
                    st.success("Post liked!")
                else:
                    st.error("You need to be logged in to like.")
            
            # Initialize the comment visibility state for this post if it's not already set
            if f"comments_visible_{post.id}" not in st.session_state:
                st.session_state[f"comments_visible_{post.id}"] = False

            # Toggle the visibility of comments
            if st.button(f"Show/Hide Comments", key=f"toggle_comments_{post.id}"):
                st.session_state[f"comments_visible_{post.id}"] = not st.session_state[f"comments_visible_{post.id}"]

            # Conditionally display the comments based on the visibility state
            if st.session_state[f"comments_visible_{post.id}"]:
                st.write("#### Comments:")
                if post.comments:
                    for comment in post.comments:
                        st.write(f"{comment.author.username}: {comment.content}")
                else:
                    st.write("No comments yet.")

                # Comment section
                comment_content = st.text_input(f"Add a comment", key=f"comment_{post.id}")
                if st.button(f"Comment", key=f"comment_btn_{post.id}"):
                    if 'logged_in' in st.session_state and st.session_state['logged_in']:
                        with SessionLocal() as db:
                            new_comment = Comment(
                                content=comment_content,
                                author_id=st.session_state['user_id'],  # The logged-in user ID
                                post_id=post.id
                            )
                            db.add(new_comment)
                            db.commit()
                            st.success("Comment added!")
                    else:
                        st.error("You need to be logged in to comment.")

            st.write("---")

        # Pagination controls
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Previous") and current_page > 0:
                st.session_state['page'] -= 1

        with col2:
            if st.button("Next") and current_page < total_pages:
                st.session_state['page'] += 1

        if os.path.exists(temp_dir):
            utility.rm_directory(temp_dir)


