resource "aws_sns_topic" "sns_error" {
  name = "watershed-sns-notifier"
}

resource "aws_sns_topic_subscription" "sns_error_sub" {
  topic_arn = aws_sns_topic.sns_error.arn
  protocol  = "email"
  endpoint  = "padmapriya.mariappan@gmail.com"

}


# resource "aws_iam_role" "sns_publish_role" {
#   name = "sns_publish_role"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Principal = {
#           Service = "cloudwatch.amazonaws.com"
#         },
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })
# }

# resource "aws_iam_policy" "sns_publish_policy" {
#   name        = "sns_publish_policy"
#   description = "A policy to allow publishing messages to the SNS topic"
#   policy      = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = "sns:Publish",
#         Resource = aws_sns_topic.sns_error.arn
#       }
#     ]
#   })
# }

# resource "aws_iam_role_policy_attachment" "attach_sns_publish_policy" {
#   role       = aws_iam_role.sns_publish_role.name
#   policy_arn = aws_iam_policy.sns_publish_policy.arn
# }











# resource "aws_sns_topic_subscription" "sns_topic_subscription" {
#   for_each = toset(["emailid1@email.com","emailid2@email.com","emailid3@email.com"])
#   topic_arn = aws_sns_topic.sns_topic.arn
#   protocol  = "email"
#   endpoint = each.value
# }
