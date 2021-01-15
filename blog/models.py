from django.db import models
from django.utils import timezone
from django import forms

# title 입력필드의 길이 체크<3
def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('글 제목은 3글자이상')


class Post(models.Model):
    #     작성자
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     글 제목
    title = models.CharField(max_length=200, validators=[min_length_3_validator])
#     글 내용
    text = models.TextField()
#     작성일
    created_date = models.DateTimeField(default=timezone.now)
#     게시일--> 값이 비어있어도 ㄱㅊ
    published_date = models.DateTimeField(blank=True,null=True)

    #  migration test--> post에 test 변수를 만들어줬기 떄문에 0002post_test가 된 것
    # test = models.TextField()



    def __str__(self):
        return self.title

    def publish(self):
        self.publshed_date = timezone.now()
        self.save()
#         승인된 댓글만 필터링하는 메서드
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)



# post 에 달린 댓글
class Comment (models.Model):
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment = True
        self.save()