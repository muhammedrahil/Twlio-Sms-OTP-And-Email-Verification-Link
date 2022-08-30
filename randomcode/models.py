# from django.db import models
# import random
# import string
# # Create your models here.

# def code_generator(size=6,chars=string.ascii_letters + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# class KirrURL(models.Model):
#     url=models.CharField(max_length=220)
#     shortcode=models.CharField(max_length=15,unique=True,blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     timestamp=models.DateTimeField(auto_now_add=True)

#     def save(self,*args,**kwarge):
#         if self.shortcode is None or self.shortcode == "":
#             self.shortcode = code_generator()
#         super(KirrURL,self).save(*args,**kwarge)


#     def __str__(self):
#         return self.url