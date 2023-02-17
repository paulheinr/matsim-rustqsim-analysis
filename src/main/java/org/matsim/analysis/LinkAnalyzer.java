package org.matsim.analysis;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.events.LinkEnterEvent;
import org.matsim.api.core.v01.events.LinkLeaveEvent;
import org.matsim.api.core.v01.events.handler.LinkEnterEventHandler;
import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
import org.matsim.api.core.v01.network.Link;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class LinkAnalyzer implements LinkEnterEventHandler, LinkLeaveEventHandler {
    private final List<LinkEnterEvent> linkEnterEventCache = new LinkedList<>();
    private final Map<Id<Link>, List<TravelTimeInformation>> travelTimesByLinkId = new HashMap<>();

    @Override
    public void handleEvent(LinkEnterEvent linkEnterEvent) {
        linkEnterEventCache.add(linkEnterEvent);
    }

    @Override
    public void handleEvent(LinkLeaveEvent linkLeaveEvent) {
        List<LinkEnterEvent> correspondingLinkEnter = this.linkEnterEventCache.stream()
                .filter(linkEnterEvent -> linkEnterEvent.getVehicleId() == linkLeaveEvent.getVehicleId()
                        && linkEnterEvent.getLinkId() == linkLeaveEvent.getLinkId()).toList();

        if (correspondingLinkEnter.isEmpty()) {
            return;
        }
        assert correspondingLinkEnter.size() == 1;
        LinkEnterEvent linkEnterEvent = correspondingLinkEnter.get(0);

        travelTimesByLinkId
                .computeIfAbsent(linkLeaveEvent.getLinkId(), id -> new LinkedList<>())
                .add(new TravelTimeInformation(linkLeaveEvent.getTime() - linkEnterEvent.getTime(), linkLeaveEvent.getTime()));

        this.linkEnterEventCache.remove(linkEnterEvent);

    }

    public void printResult() {
        for (Id<Link> linkId : travelTimesByLinkId.keySet()) {
            System.out.println("-------------------------");
            System.out.println("Link: " + linkId.toString());
            System.out.println("Travel times: " + getMetricPerHour(linkId, this::getTravelTimeAverageBetween));
            System.out.println("Traffic flow: " + getMetricPerHour(linkId, this::getTrafficFlowBetween));
        }
    }

    private Integer getTrafficFlowBetween(Id<Link> linkId, Integer begin, Integer end) {
        return Math.toIntExact(travelTimesByLinkId.get(linkId).stream()
                .filter(info -> begin <= info.timeOfLinkLeave && info.timeOfLinkLeave < end).count());
    }

    private Double getTravelTimeAverageBetween(Id<Link> linkId, Integer begin, Integer end) {
        return travelTimesByLinkId.get(linkId)
                .stream()
                .filter(info -> begin <= info.timeOfLinkLeave && info.timeOfLinkLeave < end)
                .mapToDouble(info -> info.travelTime).average()
                .orElse(0.);
    }

    private <R> List<R> getMetricPerHour(Id<Link> linkId, Function3<Id<Link>, Integer, Integer, R> getMetricBetweenTime) {
        return IntStream.range(0, 24)
                .mapToObj(hour -> {
                    int beginInSec = hour * 60 * 60;
                    int endInSec = (hour + 1) * 60 * 60;
                    return getMetricBetweenTime.apply(linkId, beginInSec, endInSec);
                })
                .collect(Collectors.toList());
    }

    public static void main(String[] args) {
        String pathToEventsFile = "./results/output_events.xml";

        EventsManager manager = EventsUtils.createEventsManager();
        LinkAnalyzer handler = new LinkAnalyzer();
        manager.addHandler(handler);
        EventsUtils.readEvents(manager, pathToEventsFile);
        handler.printResult();
    }

    private record TravelTimeInformation(double travelTime, double timeOfLinkLeave) {
        @Override
        public String toString() {
            return "{timeOfLeave: " + timeOfLinkLeave + " | travelTime: " + travelTime + "}";
        }
    }

    @FunctionalInterface
    private interface Function3<A, B, C, R> {
        public R apply(A a, B b, C c);
    }
}
