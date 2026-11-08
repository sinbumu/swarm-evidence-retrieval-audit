"""Budgeted read capability; logical API boundary, not hostile-code isolation."""
from time import perf_counter


class BudgetReader:
    def __init__(self, payloads, budget):
        started = perf_counter()
        if type(budget) is not int or budget < 0:
            raise ValueError("invalid budget")
        self.__store = {k: (v.encode("ascii") if isinstance(v, str) else v) for k, v in payloads.items()}
        if any(len(v) != 512 for v in self.__store.values()):
            raise ValueError("payload storage size mismatch")
        self.__budget = budget
        self.read = {}
        self.trace = []
        self.rejections = []
        self.costs = dict(backend_index_insertions=len(payloads), request_batches=0, requested_ids=0,
                          backend_payload_records_prepared=len(payloads), backend_payload_bytes_prepared=sum(map(len, self.__store.values())),
                          repeated_read_attempts=0, nonpublic_requests=0, rejected_batches=0,
                          reader_already_read_checks=0, reader_batch_duplicate_checks=0,
                          reader_request_set_insertions=0,
                          backend_validation_lookups=0, backend_payload_lookups=0,
                          successful_payload_batches=0, distinct_payload_reads=0, payload_bytes=0,
                          payload_read_rounds=0)
        self.preparation_seconds = perf_counter() - started
        self.lookup_seconds = 0.0

    def batch(self, ids, reason, depth=None):
        ids = list(ids)
        c = self.costs
        c["request_batches"] += 1
        c["requested_ids"] += len(ids)
        seen = set()
        repeated = 0
        for node in ids:
            c["reader_already_read_checks"] += 1
            c["reader_batch_duplicate_checks"] += 1
            if isinstance(node, str):
                repeated += int(node in self.read or node in seen)
                if node not in seen:
                    seen.add(node)
                    c["reader_request_set_insertions"] += 1
        c["repeated_read_attempts"] += repeated
        c["backend_validation_lookups"] += len(ids)
        nonpublic = sum(not isinstance(node, str) or node not in self.__store for node in ids)
        c["nonpublic_requests"] += nonpublic
        if not ids or repeated or nonpublic or len(self.read) + len(ids) > self.__budget:
            c["rejected_batches"] += 1
            self.rejections.append(dict(ids=ids, reason=reason, known_before=list(self.read)))
            raise ValueError("empty/duplicate/already-read/nonpublic/over-budget batch")
        started = perf_counter()
        values = {node: self.__store[node] for node in ids}
        self.lookup_seconds += perf_counter() - started
        c["backend_payload_lookups"] += len(ids)
        c["successful_payload_batches"] += 1
        c["payload_read_rounds"] += 1
        c["distinct_payload_reads"] += len(ids)
        c["payload_bytes"] += 512 * len(ids)
        self.trace.append(dict(round=c["payload_read_rounds"], ids=ids, reason=reason, depth=depth,
                               known_before=list(self.read), bytes=512 * len(ids)))
        self.read.update(values)
        return values
