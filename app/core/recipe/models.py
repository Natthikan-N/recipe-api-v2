from django.db import models

# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    # tags = models.ManyToManyField('Tag')
    # ingredients = models.ManyToManyField('Ingredient')
    # image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title