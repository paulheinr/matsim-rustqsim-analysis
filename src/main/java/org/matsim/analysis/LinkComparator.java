package org.matsim.analysis;

import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;

import java.io.IOException;
import java.time.Duration;
import java.util.LinkedList;
import java.util.List;

public class LinkComparator {
    private final List<LinkAnalyzer> analyzers = new LinkedList<>();

    public static void main(String[] args) throws IOException {
        LinkComparator comparator = new LinkComparator()
                .addAnalyzer("analysis_files/java_events.xml.gz", "java")
                .addAnalyzer("analysis_files/rust_events.xml", "rust");
        comparator.compareOverallTravelTimes();
    }

    public LinkComparator addAnalyzer(String path, String id) {
        EventsManager manager = EventsUtils.createEventsManager();
        analyzers.add(new LinkAnalyzer(id));
        manager.addHandler(analyzers.get(analyzers.size() - 1));
        EventsUtils.readEvents(manager, path);
        return this;
    }

    private void compareOverallTravelTimes() throws IOException {
        System.out.println("----- Overall travel time -----");
        for (LinkAnalyzer analyzer : this.analyzers) {
            System.out.println(analyzer + ": " + Duration.ofSeconds((long) analyzer.getOverallTravelTime()).toString());
            analyzer.exportResult("analysis_files/results/links_" + analyzer.getId() + ".csv");
        }
    }

}
