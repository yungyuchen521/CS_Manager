from django.db import models

# Create your models here.
class CaseModel(models.Model):
    class Meta:
        db_table = "case_model"

    id = models.AutoField(primary_key=True)

    image = models.ImageField()

class CaseResultModel(models.Model):
    class Meta:
        db_table = "case_result_model"

    id = models.AutoField(primary_key=True)
    category = models.CharField(
        max_length=32,
        choices=[
            ("bugs", "bugs"),
            ("scorch", "scorch"),
        ],
        default="bugs",
    )
    case = models.OneToOneField(
        to=CaseModel,
        on_delete=models.CASCADE,
        related_name="case_result",
    )
    result = models.TextField()
    