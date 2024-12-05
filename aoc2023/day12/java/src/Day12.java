import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

import static java.util.Collections.min;

public class Day12 {
    public static void main(String[] args) {
        System.out.println("Running...");
        long start = System.nanoTime();

        String springs;
        List<Integer> groups;

        int expand = 5;
        AtomicLong sum = new AtomicLong( 0 );
        List<Arranger> arrangers = new ArrayList<Arranger>();

        // 303
        springs = expandS( "??????????????.", expand );
        groups = expandG( Arrays.asList( 1, 1, 1, 3, 1 ), expand );
        arrangers.add( new Arranger( "303", sum, springs, groups ) );

        // 625
        springs = expandS( "?.????????????.?", expand );
        groups = expandG( Arrays.asList( 1, 3, 1 ), expand );
        arrangers.add( new Arranger( "625", sum, springs, groups ) );

        // 925
        springs = expandS( "??..??..????????", expand );
        groups = expandG( Arrays.asList( 1, 1, 2 ), expand );
        arrangers.add( new Arranger( "925", sum, springs, groups ) );

        try {
            for (Arranger value : arrangers) {
                value.start();
            }
            System.out.println( "Started " + arrangers.size() + " threads" );

            for (Arranger arranger : arrangers) {
                arranger.join();
            }
        }
        catch (InterruptedException e) {
            System.out.println( "Interrupted?" );
            throw new RuntimeException(e);
        }

        System.out.println( "Sum: " + sum );

        float timeTaken = ( System.nanoTime() - start ) / 1000f / 1000f / 1000f;
        System.out.println( "Finished in " + timeTaken + "s" );
        if ( expand == 3 ) {
            assert sum.get() == 26712645;
        }
    }

    private static String expandS(String springs, int expand) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < expand; i++) {
            out.append(springs);
            if (i < expand - 1) {
                out.append('?');
            }
        }
        return out.toString();
    }

    private static List<Integer> expandG(List<Integer> groups, int expand) {
        int newLength = groups.size() * expand;
        List<Integer> out = new ArrayList<>(newLength);
        for (int i = 0; i < newLength; i++) {
            out.add(groups.get(i % groups.size()));
        }
        return out;
    }

    private static class Arranger extends Thread {
        private final AtomicLong out;
        private final List<Integer> springs;
        private final List<Integer> groups;
        private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

        public Arranger(String name, AtomicLong out, String springs, List<Integer> groups) {
            setName( "t-arrange-" + name );

            this.out = out;
            this.groups = groups;

            List<Integer> springsList = new ArrayList<>(springs.length());
            for (int i = 0; i < springs.length(); i++) {
                char c = springs.charAt(i);
                if (c == '?') {
                    springsList.add(-1);
                }
                else if (c == '#') {
                    springsList.add(1);
                }
                else {
                    springsList.add(0);
                }
            }
            this.springs = springsList;
        }

        public void run() {
            int arrangementLength = groups.size() * 2 + 1;
            List<Integer> arrangement = new ArrayList<>(arrangementLength);
            for (int i = 0; i < arrangementLength; i++) {
                arrangement.add(-1);
            }
            long result = arrange(arrangement, springs, groups);
            long total = out.addAndGet( result );
            System.out.println( getName() + " finished, result = " + result + " total now = " + total );
        }

        private long arrange(List<Integer> arrangement, List<Integer> springs, List<Integer> groups) {
            int gs = groups.get(0);
            int ge = groups.get(groups.size() - 1);

            if (arrangement.isEmpty() || min(arrangement) >= 0) {
                return 0;
            }

            int first_unset = arrangement.indexOf(-1);
            int last_unset = arrangement.lastIndexOf(-1);

            int gaps = groups.size() + 1;
            int min_p_len = sum(groups) + gaps;
            int min_outside_space;
            if (first_unset == 0) {
                // no outer gaps needed
                min_p_len -= 2;
                min_outside_space = 0;
            }
            else {
                min_outside_space = 1;
            }

            boolean is_last = groups.size() <= 2;
            boolean is_single = groups.size() == 1;

            int used_before = sum(arrangement.subList(0, first_unset));
            int used_after = sum(arrangement.subList(last_unset + 1, arrangement.size()));
            List<Integer> remaining_springs = springs.subList(used_before, springs.size() - used_after);
            int free_len = remaining_springs.size() - min_p_len;
            if (free_len < 0) {
                return 0;
            }

            List<Integer> inner_groups;
            if (groups.size() > 2) {
                inner_groups = groups.subList(1, groups.size() - 1);
            }
            else {
                inner_groups = null;
            }

            long num_arrangements = 0;

            int max_s = min_outside_space + free_len + 1;
            for (int s = min_outside_space; s < max_s; s++) {
                if ( min_outside_space == 0 ) {
                    LocalDateTime currentDateTime = LocalDateTime.now();
                    String isoDateTime = currentDateTime.format(formatter);
                    int complete = Math.round((s - min_outside_space) / (float)max_s * 100);
                    System.out.println(isoDateTime + " " + getName() + " at " + complete + "%");
                }
                int springAt = remaining_springs.indexOf(1);
                if (springAt >= 0 && springAt < s) break;
                if (!testStart(remaining_springs, s, gs)) continue;

                int max_e = min_outside_space + free_len + 1 - (s - min_outside_space);
                for (int e = min_outside_space; e < max_e; e++) {
                    springAt = remaining_springs.lastIndexOf(1);
                    if (springAt >= remaining_springs.size() - e) break;
                    if (!testEnd(remaining_springs, e, ge)) continue;

                    if (is_last) {
                        if (is_single && (s + gs + e) < remaining_springs.size()) {
                            continue;
                        }
                        else {
                            springAt = remaining_springs.indexOf(1);
                            if (springAt >= (s + gs) && springAt <= remaining_springs.size() - (e + ge)) {
                                continue;
                            }
                        }
                    }

                    if (is_single || is_last || inner_groups == null) {
                        num_arrangements += 1;
                    }
                    else {
                        arrangement.set(first_unset, s);
                        arrangement.set(first_unset + 1, gs);
                        arrangement.set(last_unset - 1, ge);
                        arrangement.set(last_unset, e);
                        num_arrangements += arrange(arrangement, springs, inner_groups);
                        arrangement.set(first_unset, -1);
                        arrangement.set(first_unset + 1, -1);
                        arrangement.set(last_unset - 1, -1);
                        arrangement.set(last_unset, -1);
                    }
                }
            }
            return num_arrangements;
        }

        private static int sum(List<Integer> nums) {
            int sum = 0;
            for (int num : nums) {
                sum += num;
            }
            return sum;
        }

        private static boolean testStart(List<Integer> springs, int s, int gs) {
            for (int i = 0; i < s; i++) {
                if (springs.get(i) == 1) {
                    return false;
                }
            }
            for (int i = s; i < s + gs; i++) {
                if (springs.get(i) == 0) {
                    return false;
                }
            }
            return true;
        }

        private static boolean testEnd(List<Integer> springs, int e, int ge) {
            for (int i = 0; i < e; i++) {
                if (springs.get(springs.size() - i - 1) == 1) {
                    return false;
                }
            }
            for (int i = e; i < e + ge; i++) {
                if (springs.get(springs.size() - i - 1) == 0) {
                    return false;
                }
            }
            return true;
        }
    }
}
