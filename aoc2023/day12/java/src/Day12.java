import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

import static java.util.Collections.min;

public class Day12 {
    public static void main(String[] args) {
        System.out.println("Running...");
        long start = System.nanoTime();

        String springs;
        List<Integer> groups;

        int expand = 5;

        // 303
        springs = expandS( "??????????????.", expand );
        groups = expandG( Arrays.asList( 1, 1, 1, 3, 1 ), expand );
        System.out.println( "Result 303: " + begin_arrange( springs, groups ) );

        float timeTaken = ( System.nanoTime() - start ) / 1000f / 1000f / 1000f;
        System.out.println( "Finished in " + timeTaken + "s" );
    }

    private static long begin_arrange(String springs, List<Integer> groups) {
        springs = springs
                .replace('.', '_')
                .replace('?', '.');
        int arrangementLength =  groups.size() * 2 + 1;
        List<Integer> arrangement = new ArrayList<>( arrangementLength );
        for ( int i = 0; i < arrangementLength; i++ ) {
            arrangement.add( -1 );
        }
        return arrange( arrangement, springs, groups );
    }

    private static long arrange( List<Integer> arrangement, String springs, List<Integer> groups ) {
        int gs = groups.get( 0 );
        int ge = groups.get( groups.size() - 1 );

        if ( arrangement.isEmpty() || min(arrangement) >= 0 ) {
            return 0;
        }

        int first_unset = arrangement.indexOf( -1 );
        int last_unset = arrangement.lastIndexOf( -1 );

        int gaps = groups.size() + 1;
        int min_p_len = sum(groups) + gaps;
        int min_outside_space;
        if ( first_unset == 0 ) {
            // no outer gaps needed
            min_p_len -= 2;
            min_outside_space = 0;
        }
        else {
            min_outside_space = 1;
        }

        boolean is_last = groups.size() <= 2;
        boolean is_single = groups.size() == 1;

        int used_before = sum(arrangement.subList(0, first_unset ) );
        int used_after = sum(arrangement.subList(last_unset + 1, arrangement.size() ) );
        String remaining_springs = springs.substring(used_before, springs.length() - used_after);
        int free_len = remaining_springs.length() - min_p_len;
        if ( free_len < 0 ) {
            return 0;
        }

        List<Integer> inner_groups;
        if ( groups.size() > 2 ) {
            inner_groups = groups.subList(1, groups.size() - 1 );
        }
        else {
            inner_groups = null;
        }

        long num_arrangements = 0;
        for ( int s = min_outside_space; s < min_outside_space + free_len + 1; s++ ) {
            int springAt = remaining_springs.indexOf('#');
            if ( springAt >= 0 && springAt < s ) break;

            String test_s = "_".repeat( s ) + "#".repeat( gs );
            boolean test_s_match = Pattern.matches( remaining_springs.substring( 0, test_s.length() ), test_s );
            if ( !test_s_match ) {
                continue;
            }

            for ( int e = min_outside_space; e < min_outside_space + free_len + 1 - (s - min_outside_space); e++ ) {
                springAt = remaining_springs.lastIndexOf( '#' );
                if ( springAt >= remaining_springs.length()-e ) break;
                String test_e = "#".repeat( ge ) + "_".repeat( e );
                boolean test_e_match = Pattern.matches(
                        remaining_springs.substring( remaining_springs.length()-test_e.length() ),
                        test_e );

                if ( test_e_match ) {
                    if ( is_last ) {
                        if ( is_single && s + gs + e < remaining_springs.length() ) {
                            continue;
                        }
                        else {
                            springAt = remaining_springs.indexOf( '#' );
                            if ( springAt >= test_s.length() && springAt <= remaining_springs.length() - test_e.length() ) {
                                continue;
                            }
                        }
                    }

                    if ( is_single ) {
                        num_arrangements += 1;
                    }
                    else if ( is_last ) {
                        num_arrangements += 1;
                    }
                    else if ( inner_groups == null ) {
                        num_arrangements += 1;
                    }
                    else {
                        arrangement.set( first_unset, s );
                        arrangement.set( first_unset + 1, gs );
                        arrangement.set( last_unset - 1, ge );
                        arrangement.set( last_unset, e );
                        num_arrangements += arrange( arrangement, springs, inner_groups );
                        arrangement.set( first_unset, -1 );
                        arrangement.set( first_unset + 1, -1 );
                        arrangement.set( last_unset - 1, -1 );
                        arrangement.set( last_unset, -1 );
                    }
                }
            }
        }
        return num_arrangements;
    }

    private static int sum( List<Integer> nums ) {
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        return sum;
    }

    private static String expandS(String springs, int expand) {
        StringBuilder out = new StringBuilder();
        for ( int i = 0; i < expand; i++ ) {
            out.append(springs);
            if ( i < expand - 1 ) {
                out.append('?');
            }
        }
        return out.toString();
    }

    private static List<Integer> expandG(List<Integer> groups, int expand) {
        int newLength = groups.size() * expand;
        List<Integer> out = new ArrayList<>(newLength);
        for ( int i = 0; i < newLength; i++ ) {
            out.add(groups.get( i % groups.size() ) );
        }
        return out;
    }
}
