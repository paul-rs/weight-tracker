aws cloudformation deploy --stack-name weight-tracker-dev \
    --template-file ./cf/weight_tracker.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides Stage=dev \
    --tags Stage=dev Domain=weight-tracker