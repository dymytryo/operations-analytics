# Project Management Order-Picking System

Portfolio project applying PERT/CPM project management analysis to an automated order-picking system implementation.

## Project Focus

R.C. Coleman needed to automate warehouse order-picking operations with a computerized order-picking system and conveyor process. Management wanted the project completed in 40 weeks, so the analysis focused on whether the schedule was feasible and what timeline reduction would be needed to reach a high-confidence delivery target.

The portfolio version focuses on the operations analytics work:

- Defining project activities, predecessors, and time estimates
- Calculating expected activity durations with PERT
- Running forward and backward pass schedule analysis
- Identifying the critical path with zero-slack activities
- Estimating schedule risk through variance, standard deviation, and completion probability
- Recommending schedule crashing for critical-path activities

## Method

PERT was used to convert optimistic, most likely, and pessimistic estimates into expected activity durations. CPM was then used to calculate early start, early finish, late start, late finish, slack, and the critical path. Project variance was calculated from critical-path activity variances to estimate the probability of meeting the 40-week target.

```mermaid
flowchart LR
    A[Activity list and predecessors] --> B[PERT expected durations]
    B --> C[Forward pass]
    C --> D[Backward pass]
    D --> E[Critical path and slack]
    E --> F[Variance and completion probability]
    F --> G[Crash critical-path activities]
```

## Key Result

The expected project duration was 43 weeks, which was 3 weeks longer than management's 40-week target. The critical path was:

`B -> C -> E -> F -> H -> J -> K`

The probability of finishing within 40 weeks was only 10.38%, based on a project standard deviation of 2.38 weeks. To reach an 80% probability of completion within 40 weeks, the expected duration needed to be reduced to roughly 38 weeks.

| Metric | Value |
| --- | ---: |
| Management target | 40 weeks |
| Expected project duration | 43 weeks |
| Critical path variance | 5.666 |
| Project standard deviation | 2.38 weeks |
| Probability of finishing in 40 weeks | 10.38% |
| Expected duration needed for 80% confidence | 38 weeks |

## Project Contents

- [data/activity_estimates.csv](data/activity_estimates.csv) - activity predecessors and PERT estimates
- [data/schedule_analysis.csv](data/schedule_analysis.csv) - forward/backward pass and slack analysis
- [data/project_risk_summary.csv](data/project_risk_summary.csv) - critical path, variance, and completion probability metrics
- [diagrams/project_workflow.mmd](diagrams/project_workflow.mmd) - Mermaid workflow diagram
- [docs/project-summary.md](docs/project-summary.md) - concise project context and portfolio notes

## Skills Demonstrated

- Project management analytics
- PERT expected-time estimation
- Critical Path Method
- Forward and backward pass calculations
- Slack analysis
- Schedule risk and probability estimation
- Project crashing recommendation

## Publishing Note

The original Word document is intentionally excluded from the public portfolio because it includes classroom-report formatting and embedded document artifacts that are not needed for a concise portfolio presentation. This project keeps only the cleaned, derived artifacts needed to explain the work professionally.
