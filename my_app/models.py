from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validate(self,formData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(formData["first_name"]) < 2:
            errors["first_name"] = "First Name should be at least 2 character"
        if len(formData["last_name"]) < 2:
            errors["last_name"] = "Last Name should be at least 2 character"
        if len(formData["email"]) < 2:
            errors["email"] = "email should be at least 2 characters"
        if len(formData["password"]) < 2:
            errors["password"] = "password should be at least 2 characters"
        if formData["confirm_password"] != formData["password"]:
            errors["confirm_password"] = "confirm pw should match password"
        if not EMAIL_REGEX.match(formData['email']):
            errors['invalid_email'] = 'Invalid Email Address'
        email_check = self.filter(email=formData['email'])
        if email_check:
            errors['email_in_use'] = "Email already in use"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # user_posts
    # liked_posts
    # comments


class Facebook_Post(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    # post_comments

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    facebook_post = models.ForeignKey(Facebook_Post, related_name="post_comments", on_delete=models.CASCADE)

