# Commerce verifier design

This technical note was drafted with AI assistance. It does not replace the author's required human-written README sections, and it does not claim the task defeats current models.

## Why greedy allocation can be wrong

Two purchases have prices 100 and 110. Two returns have prices 105 and 100, in that order. All quantities are one, the price tolerance is five, and all timestamps are eligible. The first return can use either purchase. The second can use only the 100 purchase. Allocating the first return to the 100 purchase leaves one unit unmatched. Reserving that purchase for the second return matches both. The verifier includes this case.

## Exact priorities

Quantity is optimized first by augmenting flow until no additional unit can be matched. Cost is optimized among flows of that quantity. If T is the total return quantity and W is the time window, every feasible allocation has total age between zero and T times W. Therefore using cost `price_difference * (T*W + 1) + age` ensures that reducing price distance by one always outweighs any possible worsening of total age. All quantities, prices, and costs are integers. No numerical tolerance is needed.

The task accepts all allocations tied on quantity, price distance, and age. Those allocations can yield different refund amounts if they select different returns. Refund and net amounts are checked against each submitted allocation, rather than forced to match a particular reference allocation.

## How the verifier proves optimality

The submitted allocations first undergo ordinary checks: eligible pairs, positive integer quantities, no duplicate pairs, no exceeded purchase or return capacity, correct audit records, and correct totals.

A residual graph represents legal changes to the submitted allocation. Forward edges represent unused capacity. Reverse edges represent removing an existing allocation. If a path connects the source to the sink, additional quantity can be matched, so the submitted allocation is not maximal.

Once quantity is maximal, any alternative feasible flow of the same quantity differs by residual cycles. A cycle with negative cost is an improvement in price distance or age. Conversely, absence of a negative-cost cycle certifies minimum cost for that flow quantity. The verifier uses Bellman-Ford relaxation from zero distances at every vertex to detect negative cycles anywhere in the graph. It performs these checks separately for each customer/SKU group because no eligible edges cross groups.

The reference solver constructs an allocation using successive shortest augmenting paths. The verifier checks a submitted allocation's residual graph instead of invoking that solver. Small generated cases additionally enumerate each return unit's eligible destinations, including leaving it unmatched, and compare the resulting best objective tuple. This third method checks the cost encoding and graph-based verification against exhaustive answers on small histories.

## Scope of evidence

Oracle and nop Docker validation demonstrate that the reference passes and the incorrect starter fails. They do not establish model difficulty. Both GPT-6.1 Sol and Opus 5.5 completed and passed their first trials; this candidate does not satisfy the hiring-email requirement for three failures from either configuration.
