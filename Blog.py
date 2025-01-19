import tkinter as tk
from tkinter import messagebox, simpledialog

# File path to store blog posts
BLOG_FILE = "blog_posts.txt"


# Function to load posts from the file
def load_posts():
    posts = []
    try:
        with open(BLOG_FILE, "r") as file:
            content = file.read().strip()
            if content:
                post_entries = content.split("\n\n")
                for post_entry in post_entries:
                    title, content = post_entry.split("\n", 1)
                    posts.append({"title": title, "content": content})
    except FileNotFoundError:
        pass
    return posts


# Function to save posts to the file
def save_posts():
    with open(BLOG_FILE, "w") as file:
        for post in blog_posts:
            file.write(post["title"] + "\n")
            file.write(post["content"] + "\n\n")


# In-memory storage for blog posts
blog_posts = load_posts()


# Function to create a new post
def create_post():
    title = simpledialog.askstring("New Post", "Enter the title of your post:")
    if not title:
        messagebox.showwarning("Warning", "Title cannot be empty!")
        return

    content_window = tk.Toplevel(root)
    content_window.title("Write Post Content")
    content_window.geometry("400x300")

    tk.Label(content_window, text="Write your content below:", font=("Arial", 12)).pack(pady=10)
    content_text = tk.Text(content_window, wrap=tk.WORD, font=("Arial", 12))
    content_text.pack(expand=True, fill=tk.BOTH)

    def save_post():
        content = content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Content cannot be empty!")
            return

        # Save the post to the in-memory list
        blog_posts.append({"title": title, "content": content})
        save_posts()  # Save the posts to file
        messagebox.showinfo("Success", "Post saved successfully!")
        content_window.destroy()
        display_posts()

    tk.Button(content_window, text="Save Post", command=save_post).pack(pady=10)


# Function to edit a post
def edit_post(post):
    content_window = tk.Toplevel(root)
    content_window.title(f"Edit {post['title']}")
    content_window.geometry("400x300")

    tk.Label(content_window, text="Edit your content below:", font=("Arial", 12)).pack(pady=10)
    content_text = tk.Text(content_window, wrap=tk.WORD, font=("Arial", 12))
    content_text.insert("1.0", post["content"])
    content_text.pack(expand=True, fill=tk.BOTH)

    def save_edited_post():
        edited_content = content_text.get("1.0", tk.END).strip()
        if not edited_content:
            messagebox.showwarning("Warning", "Content cannot be empty!")
            return

        # Update the post in memory
        post["content"] = edited_content
        save_posts()  # Save the posts to file
        messagebox.showinfo("Success", "Post edited successfully!")
        content_window.destroy()
        display_posts()

    tk.Button(content_window, text="Save Edited Post", command=save_edited_post).pack(pady=10)


# Function to view a post
def view_post(post):
    post_window = tk.Toplevel(root)
    post_window.title(post["title"])
    post_window.geometry("400x300")

    tk.Label(post_window, text=post["title"], font=("Arial", 16, "bold")).pack(pady=10)
    content_text = tk.Text(post_window, wrap=tk.WORD, font=("Arial", 12))
    content_text.insert("1.0", post["content"])
    content_text.configure(state=tk.DISABLED)
    content_text.pack(expand=True, fill=tk.BOTH)

    # Delete post button
    def delete_post():
        if messagebox.askyesno("Delete Post", "Are you sure you want to delete this post?"):
            blog_posts.remove(post)
            save_posts()  # Save the updated list to file
            messagebox.showinfo("Deleted", "Post deleted successfully!")
            post_window.destroy()
            display_posts()

    # Edit post button
    def edit_existing_post():
        edit_post(post)

    tk.Button(post_window, text="Delete Post", command=delete_post, font=("Arial", 12), bg="red").pack(pady=10)
    tk.Button(post_window, text="Edit Post", command=edit_existing_post, font=("Arial", 12), bg="blue").pack(pady=10)


# Function to display all posts on the homepage
def display_posts():
    for widget in post_list_frame.winfo_children():
        widget.destroy()

    if blog_posts:
        for post in blog_posts:
            post_button = tk.Button(
                post_list_frame,
                text=post["title"],
                font=("Arial", 12),
                command=lambda p=post: view_post(p),
                anchor="w"
            )
            post_button.pack(fill=tk.X, pady=2, padx=10)
    else:
        tk.Label(post_list_frame, text="No posts available. Create one!", font=("Arial", 12)).pack(pady=10)


# Main application window
root = tk.Tk()
root.title("Simple Blog Application")
root.geometry("500x400")

# Header
tk.Label(root, text="Welcome to Simple Blog", font=("Arial", 18, "bold")).pack(pady=10)

# Frame for listing posts
post_list_frame = tk.Frame(root)
post_list_frame.pack(expand=True, fill=tk.BOTH)

# Buttons for actions
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=10)

tk.Button(button_frame, text="Create New Post", command=create_post, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Refresh Posts", command=display_posts, font=("Arial", 12)).pack(side=tk.RIGHT, padx=10)

# Initial display of posts
display_posts()

# Start the application
root.mainloop()
