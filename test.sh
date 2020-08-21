PROJECTVERSION=$(cookietemple bump-version --project-version . | tail -n1)
echo $PROJECTVERSION;
if [[ $PROJECTVERSION == *"SNAPSHOT"* ]];then
    exit -1
else
    exit 0
fi
