package org.matsim.analysis;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.network.Link;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class LinkComparator {
    private final List<LinkAnalyzer> analyzers = new LinkedList<>();
    private IdMappings idMappings;

    public static void main(String[] args) throws IOException {
        LinkComparator comparator = new LinkComparator("analysis_files/id_mappings.json")
                .addAnalyzer("analysis_files/java_events.xml.gz", "java")
                .addAnalyzer("analysis_files/rust_events.xml", "rust", true);
        comparator.compareOverallTravelTimes();
    }

    public LinkComparator(String pathToMappings) throws IOException {
        String json = Files.readString(Path.of(pathToMappings));
        idMappings = new ObjectMapper().readValue(json, IdMappings.class);
    }

    public LinkComparator addAnalyzer(String path, String id) {
        return addAnalyzer(path, id, false);
    }

    public LinkComparator addAnalyzer(String path, String id, boolean mapFromInternalToMatsim) {
        EventsManager manager = EventsUtils.createEventsManager();
        LinkAnalyzer analyzer = new LinkAnalyzer(id);
        if (mapFromInternalToMatsim) {
            analyzer.setIdMappings(this.idMappings);
        }

        analyzers.add(analyzer);

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

    private void compareAggregatedTravelTimesPerHour() {
        assert analyzers.size() == 2;
        Set<Id<Link>> allIdsWithTravelTimes = analyzers.stream()
                .map(LinkAnalyzer::getTravelTimeAveragesPerLink)
                .map(HashMap::keySet)
                .flatMap(Set::stream)
                .collect(Collectors.toSet());

        HashMap<Id<Link>, Double[]> absoluteTravelTimeDifferences = new HashMap<>();

        for (Id<Link> linkId : allIdsWithTravelTimes) {
            var travelTimes1 = analyzers.get(0).getTravelTimeAveragesPerLink()
                    .getOrDefault(linkId, IntStream.range(0, 24).mapToObj(Double::valueOf).toList()).toArray(new Double[24]);
            var travelTimes2 = analyzers.get(1).getTravelTimeAveragesPerLink()
                    .getOrDefault(linkId, IntStream.range(0, 24).mapToObj(Double::valueOf).toList()).toArray(new Double[24]);
            var result = new Double[24];
            Arrays.setAll(result, i -> Math.abs(travelTimes1[i] - travelTimes2[i]));
            absoluteTravelTimeDifferences.put(linkId, result);
        }
        

    }

}
