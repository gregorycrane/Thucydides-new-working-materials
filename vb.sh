egrep ">[VP]" thucunimorphs.txt | egrep "\t2\.00[2-6]" | awk -F '\t' '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $7}' | sort -rn | uniq -c  | more > thuc2.2-6-verbs
egrep ">[VP]" thucunimorphs.txt | egrep "\t2\.00[2-6]" | awk -F '\t' '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $7 "\t" $11}' | sort -rn | uniq -c  | more > thuc2.2-6-vparad
egrep -f genders thucunimorphs.txt | fgrep -v ">P" | egrep "\t2\.00[2-8]" | awk -F '\t' '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $7 "\t" $11}' | sort -rn | uniq -c  | more > thuc2.2-6-nparad.txt
egrep " ind " thucunimorphs.txt |  egrep "\t2\.00[2-8]" | awk -F '\t' '{print $1 "\t" $2 "\t" $3 "\t" $5 "\t" $7 "\t" $11}' | sort -rn | uniq -c  | more > thuc2.2-6-nparad.txt
