#!/usr/bin/perl
while(<>) {
	@a = split('\t');
        #if( @a[4] == 'σύν' and @a[5] =~ /([0-9])/ ) {
        if( @a[4] eq 'σύν' ) {
		$prep[@a[4].'-'.$1]++;
		print(@a[4],"\n");
		print $_;
	}
}

foreach my $tmp (keys %prep) {
	print("$tmp\t$prep[$tmp]\n");
}
