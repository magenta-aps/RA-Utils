import hypothesis.strategies as st

def deferred_hashable():
    return st.one_of(*base_strategies, *recursive_strategies)

base_strategies = [
    st.binary(),
    st.booleans(),
    st.characters(),
    st.complex_numbers(allow_nan=False),
    st.dates(),
    st.datetimes(),
    st.decimals(allow_nan=False),
    st.emails(),
    st.floats(allow_nan=False),
    st.fractions(),
    st.functions(),
    st.integers(),
    st.ip_addresses(),
    st.none(),
    st.text(),
    st.timedeltas(),
    st.times(),
    # st.timezone_keys(),
    # st.timezones(),
    st.uuids(),
]
non_hashable_strategies = [
    st.slices(1),
    st.dictionaries(keys=st.deferred(deferred_hashable), values=st.deferred(deferred_hashable)),
    st.lists(st.deferred(deferred_hashable)),
    st.sets(st.deferred(deferred_hashable)),
]
recursive_strategies = [
    st.frozensets(st.deferred(deferred_hashable)),
    st.iterables(st.deferred(deferred_hashable)),
    st.tuples(st.deferred(deferred_hashable)),
]
any_strategy = st.one_of(*base_strategies, *recursive_strategies, *non_hashable_strategies)
