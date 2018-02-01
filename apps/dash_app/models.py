from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import time
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

def num_check(name):
    #checks if the entered password meets our requirements
    has_num = False

    for char in name:
        if char.isdigit():
            has_num = True

    return has_num


def has_upper_num(password):
    #checks if the entered password meets our requirements
    has_upper = False
    has_num = False
    check = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.isdigit():
            has_num = True

    if has_num and has_upper:
        check = True

    return check


class UserManager(models.Manager):
    def registration_validation(self, postData):
        print postData
        errors = {}
        for thing in postData:
            print thing
            if len(postData[thing]) < 1:
                errors['submit'] = "All fields required"
                return (True, errors)
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"
                return (True, errors)

        print errors
        if len(postData['f_name']) < 2:
            errors['f_name'] = "Name should be more than 2 characters"

        if len(postData['l_name']) < 2:
            errors['l_name'] = "Name should be more than 2 characters"

        if num_check(postData['f_name']):
           errors['f_name'] = "Names must only contain letters"

        if num_check(postData['l_name']):
            errors['l_name'] = "Names must only contain letters"

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"

        if len(postData['pwd']) < 8:
            errors["pwd"] = "Password must be at least 8 characters"

        if not has_upper_num(postData['pwd']):
            errors["pwd"] = "Password must contain at least one uppercase letter and one number"

        if postData['pwd_c'] != postData['pwd']:
            errors["pwd_c"] = "Passwords must match"

        records = User.objects.filter(email=postData['email'])

        if len(records) > 0:
            errors["email"] = "Account already exists for this email"

        print errors
        if len(errors) > 0:
            return (True,errors)

        else: 
            new_pwd = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(email=postData['email'], first_name=postData['f_name'], last_name=postData['l_name'], password=new_pwd)
            new_id = new_user.id
            return (False,new_id)

    def login_validation(self, postData):
        errors = {}
        for thing in postData:
            print postData[thing]
            if len(postData[thing]) < 1:
                errors[thing] = "All fields required"
                return (True, errors)
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"
                return (True, errors)
            
        records = User.objects.filter(email=postData['email'])

        if len(records) > 0:
            pwd = records[0].password
            check = bcrypt.checkpw(postData['pwd'].encode(), pwd.encode())
            if check:
                return (False, records[0].id)
            else:
                errors["pwd"] = "Incorrect user/password"
                return (True, errors)
        else:
            errors["email"] = "Account doesn't exist for this email. Please register."
            return (True, errors)

    def update_validation(self, postData, user_id):
        errors = {}
        for thing in postData:
            if len(postData[thing]) < 1:
                errors['submit'] = "All fields required"
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"

        if len(errors) > 0:
            return (True, errors)
        print postData['type']
        
        if postData['type'] == 'information':
            if len(postData['f_name']) < 2:
                errors['f_name'] = "Name should be more than 2 characters"

            if len(postData['l_name']) < 2:
                errors['l_name'] = "Name should be more than 2 characters"

            if num_check(postData['f_name']):
                errors['f_name'] = "Names must only contain letters"

            if num_check(postData['l_name']):
                errors['l_name'] = "Names must only contain letters"

            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "Invalid email address"

            records = User.objects.filter(email=postData['email'])

            if len(records) > 0:
                errors["email"] = "Account already exists for this email"

            if len(errors) > 0:
                return (True, errors)

            edit_user = User.objects.get(id=user_id)
            edit_user.first_name = postData['f_name']
            edit_user.last_name = postData['l_name']
            edit_user.email = postData['email']
            edit_user.save()
            return (False, "Successfully updated information")
            
        elif postData['type'] == 'password':
            if len(postData['pwd']) < 8:
                errors["pwd"] = "Password must be at least 8 characters"

            if not has_upper_num(postData['pwd']):
                errors["pwd"] = "Password must contain at least one uppercase letter and one number"

            if postData['pwd_c'] != postData['pwd']:
                errors["pwd_c"] = "Passwords must match"
            
            if len(errors) > 0:
                return (True, errors)

            new_pwd = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
            edit_user = User.objects.get(id=user_id)
            edit_user.password = new_pwd
            edit_user.save()
            return (False, "Successfully updated password")

        elif postData['type'] == 'description':
            edit_user = User.objects.get(id=user_id)
            print edit_user
            edit_user.desc = postData['desc']
            edit_user.save()
            return (False, "Successfully updated description")


        else:
            errors['type'] = "Processing error. Invalid submission."
            return (True, errors)

    def admin_update_validation(self, postData, user_id):
        errors = {}
        for thing in postData:
            if len(postData[thing]) < 1:
                errors['submit'] = "All fields required"
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"

        if len(errors) > 0:
            return (True, errors)

        if postData['type'] == 'information':
            if len(postData['f_name']) < 2:
                errors['f_name'] = "Name should be more than 2 characters"

            if len(postData['l_name']) < 2:
                errors['l_name'] = "Name should be more than 2 characters"

            if num_check(postData['f_name']):
                errors['f_name'] = "Names must only contain letters"

            if num_check(postData['l_name']):
                errors['l_name'] = "Names must only contain letters"

            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "Invalid email address"

            records = User.objects.filter(email=postData['email'])

            if len(records) > 0:

                if records[0].email != postData['email']:
                    errors["email"] = "Account already exists for this email"
            
            if postData['user_level'] != 'normal' and postData['user_level'] != 'admin':
                errors['user_level'] = "Invalid user level entered"

            if len(errors) > 0:
                return (True, errors)
            
            print postData
            edit_user = User.objects.get(id=user_id)
            edit_user.first_name = postData['f_name']
            edit_user.last_name = postData['l_name']
            edit_user.email = postData['email']
            edit_user.user_level = postData['user_level']
            edit_user.save()
            print edit_user.user_level
            return (False, "Successfully updated information")

        elif postData['type'] == 'password':
            if len(postData['pwd']) < 8:
                errors["pwd"] = "Password must be at least 8 characters"

            if not has_upper_num(postData['pwd']):
                errors["pwd"] = "Password must contain at least one uppercase letter and one number"

            if postData['pwd_c'] != postData['pwd']:
                errors["pwd_c"] = "Passwords must match"

            if len(errors) > 0:
                return (True, errors)

            new_pwd = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
            edit_user = User.objects.get(id=user_id)
            edit_user.password = new_pwd
            edit_user.save()
            return (False, "Successfully updated password")

        else:
            errors['type'] = "Processing error. Invalid submission."
            return (True, errors)


    def is_admin(self, user_id):
        check = User.objects.get(id=user_id)
        if check.user_level == 'admin':
            return (True, "admin")
        else:
            return (False, "Permission denied, access level insufficient")
    
    def delete_user(self, user_id):
        get_user = User.objects.filter(id=user_id)

        if len(get_user) > 0:
            get_user.delete()
            return(True,"Successfully deleted record")

        else:
            return(False, "Couldn't delete record, out of range.")


class MessageManager(models.Manager):
    def message_validation(self, postData, user_id, session_id):
        errors = {}
        for thing in postData:
            if len(postData[thing]) < 1:
                errors['submit'] = "Message field blank"
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"

        if len(errors) > 0:
            return (True, errors)

        new_message = Message.objects.create(message=postData['message'])
        rel_receiver = User.objects.get(id=user_id)
        rel_poster = User.objects.get(id=session_id)
        new_message.receiver = rel_receiver
        new_message.poster = rel_poster
        new_message.save()
        return (False, "Successfully updated information")

    def delete_messages(self, user_id):
        get_messages = Message.objects.filter(poster=user_id)

        if len(get_messages) > 0:
            get_messages.delete()
            return(True, "Successfully deleted messages")

        else:
            return(False, "Couldn't delete messages")


class CommentManager(models.Manager):
    def comment_validation(self, postData, user_id):
        errors = {}
        for thing in postData:
            if len(postData[thing]) < 1:
                errors['submit'] = "Comment field blank"
            if len(postData[thing]) > 255:
                errors[thing] = "Exceeded field length"

        if len(errors) > 0:
            return (True, errors)
        
        new_comment = Comment.objects.create(comment=postData['comment'])
        rel_msg = Message.objects.get(id=postData['rel_message'])
        rel_commentor = User.objects.get(id=user_id)
        new_comment.message = rel_msg
        new_comment.commentor = rel_commentor
        new_comment.save()
        return (False, "Successfully updated information")

    def delete_comments(self, user_id):
        get_comments = Comment.objects.filter(commentor=user_id)
        print get_comments
        if len(get_comments) > 0:
            get_comments.delete()
            return(True, "Successfully deleted comments")

        else:
            return(False, "Couldn't delete comments")


class User(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=10,default='normal')
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User object: id='{}' email='{}' first_name='{}' last_name='{}' user_level='{}' desc='{}' created='{}'>".format(self.id, self.email, self.first_name, self.last_name, self.user_level, self.desc, self.created_at)


class Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="messages_posted", null=True)
    receiver = models.ForeignKey(User, related_name="messages_received", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __repr__(self):
        return "<Message object: id='{}' message='{}' poster='{}' receiver='{}' created='{}'>".format(self.id, self.message, self.poster, self.receiver, self.created_at)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name='comments', null=True)
    commentor = models.ForeignKey(User, related_name='comments_posted', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __repr__(self):
        return "<Comment object: id='{}' comment='{}' message='{}' commentor='{}' created='{}'>".format(self.id, self.comment, self.message, self.commentor, self.created_at)
