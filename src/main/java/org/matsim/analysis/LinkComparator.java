package org.matsim.analysis;

import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.events.EventsUtils;

import java.io.IOException;

public class LinkComparator {
    public static void main(String[] args) throws IOException {
        String pathToEventsFile = "./results/output_events.xml";

        EventsManager manager = EventsUtils.createEventsManager();
        LinkAnalyzer handler = new LinkAnalyzer();
        manager.addHandler(handler);
        EventsUtils.readEvents(manager, pathToEventsFile);
        handler.printResult();
        handler.exportResult();
    }
    

}
