package org.matsim.analysis;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.events.LinkEnterEvent;
import org.matsim.api.core.v01.events.LinkLeaveEvent;
import org.matsim.api.core.v01.events.handler.LinkEnterEventHandler;
import org.matsim.api.core.v01.events.handler.LinkLeaveEventHandler;
import org.matsim.api.core.v01.network.Link;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;

import java.util.*;

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
            System.out.println("Travel times: " + travelTimesByLinkId.get(linkId));
            System.out.println("Traffic flow: " + Arrays.toString(getTrafficFlowPerHour(linkId)));
        }
    }

    private int[] getTrafficFlowPerHour(Id<Link> linkId) {
        int[] result = new int[24];
        for (int i = 0; i < 24; i++) {
            int beginInSec = i * 60 * 60;
            int endInSec = (i + 1) * 60 * 60;
            result[i] = (int) travelTimesByLinkId.get(linkId).stream()
                    .filter(info -> beginInSec <= info.timeOfLinkLeave && info.timeOfLinkLeave < endInSec).count();
        }
        return result;
    }

    public static void main(String[] args) {
        String pathToEventsFile = "./results/output_events.xml";

        EventsManager manager = EventsUtils.createEventsManager();
        LinkAnalyzer handler = new LinkAnalyzer();
        manager.addHandler(handler);
        EventsUtils.readEvents(manager, pathToEventsFile);
        handler.printResult();
    }

    private record TravelTimeInformation(Double travelTime, Double timeOfLinkLeave) {
        @Override
        public String toString() {
            return travelTime.toString();
        }
    }
}
