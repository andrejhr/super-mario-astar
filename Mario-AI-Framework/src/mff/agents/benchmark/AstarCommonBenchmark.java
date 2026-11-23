package mff.agents.benchmark;

import mff.agents.astar.AStarTree;
import mff.agents.astar.Agent;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import static mff.LevelLoader.getLevel;

public class AstarCommonBenchmark {

    public static void main(String[] args) throws IOException {
        String searchSteps = args[0];
        String ttfw = args[1];
        Agent.SEARCH_STEPS = Integer.parseInt(searchSteps);
        AStarTree.TIME_TO_FINISH_WEIGHT = Float.parseFloat(ttfw);

        new File("agent-benchmark").mkdir();
        String fileName = "agent-benchmark" + File.separator + "astar-SS-" + searchSteps + "-TTFW-" + ttfw + ".csv";
        FileWriter writer = new FileWriter(fileName);
        writer.write("searchSteps,ttfw,level,win/fail,% travelled,run time,game ticks,planning time,total plannings,nodes evaluated,most backtracked nodes\n");

        String params = searchSteps + "," + ttfw;

        warmup();

        for (int i = 1; i <= 15; i++) {
            runLevel(writer, params, "original", i, 200);
        }
        for (int i = 1; i <= 15; i++) {
            runLevel(writer, params, "krys", i, 30);
        }
        for (int i = 1; i <= 15; i++) {
            runLevel(writer, params, "patternCount", i, 30);
        }

        writer.close();
    }

    private static void warmup() {
        System.out.println("WARMUP");
        String level = getLevel("./levels/original/lvl-1.txt");
        AgentBenchmarkGame game = new AgentBenchmarkGame();
        game.runGame(new Agent(), level, 200, 0, false);
    }

    private static void runLevel(FileWriter writer, String params, String levelPack, int number, int timer) throws IOException {
        System.out.println(levelPack + "-" + number);
        String level = getLevel("./levels/" + levelPack + "/lvl-" + number + ".txt");
        AgentBenchmarkGame game = new AgentBenchmarkGame();
        Agent agent = new Agent();
        AgentStats stats = game.runGame(agent, level, timer, 0, false);

        writer.write(params + ","
                + levelPack + "-" + number + ","
                + stats.win + ","
                + stats.percentageTravelled + ","
                + stats.runTime + ","
                + stats.totalGameTicks + ","
                + stats.totalPlanningTime + ","
                + stats.searchCalls + ","
                + stats.nodesEvaluated + ","
                + agent.getMostBacktrackedNodes() + "\n");
        writer.flush();
    }
}
