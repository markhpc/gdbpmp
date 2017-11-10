# gdbpmp - A GDB Based Wallclock Profiler

gdbpmp is a wall clock time-based profiler based loosely on Mak 
Nazečić-Andrlon's gdbprof.

### Rationale

gdbpmp expands on gdbprof in a number of ways:  

 * gdbpmp can be run from the command-line or from inside GDB.
 * It can gather samples from multiple threads.
 * Sample data can be saved and viewed at a later time.
 * Samples are gathered independently for every thread.
 * Filters can be used to limit which threads samples are gathered from.
 * CTRL+C can be used to stop sample gathering along with a specified number of samples to collect before exiting.

### Caveats

Some features are still being implemented.  KeyboardInterrupt handling still
a bit wonky.  Not many options for changing the callgraph view yet.

### Help
```
usage: gdbpmp.py [-h] (-i INPUT | -p PID) [-s SLEEP] [-n SAMPLES] [-m MATCH]
                 [-x EXCLUDE] [-o OUTPUT] [-g GDB_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Read collected samples from this file.
  -p PID, --pid PID     PID of the process to connect to.
  -s SLEEP, --sleep SLEEP
                        Period of time to sleep between samples in seconds.
  -n SAMPLES, --samples SAMPLES
                        The number of samples to collect.
  -m MATCH, --match MATCH
                        A comma separated list of strings to match with
                        threads
  -x EXCLUDE, --exclude EXCLUDE
                        A comma separated list of strings to match when
                        excluding threads.
  -o OUTPUT, --output OUTPUT
                        Write collected samples to this file.
  -g GDB_PATH, --gdb_path GDB_PATH
                        Path to the GDB executable.
```
### Example
```
$ ./gdbpmp.py -p 18965 -n 100 -m bstore_kv_sync,bstore_kv_final -o gdbpmp.data
Attaching to process 18965...Done.
Gathering Samples.............................................................
.......................................
Profiling complete with 100 samples.
```
```
$ ./gdbpmp.py -i gdbpmp.data


Thread: 1 (ceph-osd) - 0 samples 


Thread: 2 (signal_handler) - 0 samples 


Thread: 3 (osd_srv_agent) - 0 samples 


Thread: 4 (safe_timer) - 0 samples 


Thread: 5 (safe_timer) - 0 samples 


Thread: 6 (safe_timer) - 0 samples 


Thread: 7 (safe_timer) - 0 samples 


Thread: 8 (finisher) - 0 samples 


Thread: 9 (fn_anonymous) - 0 samples 


Thread: 10 (osd_srv_heartbt) - 0 samples 


Thread: 11 (tp_osd_cmd) - 0 samples 


Thread: 12 (tp_osd_disk) - 0 samples 


Thread: 13 (tp_osd_tp) - 0 samples 


Thread: 14 (tp_osd_tp) - 0 samples 


Thread: 15 (tp_osd_tp) - 0 samples 


Thread: 16 (tp_osd_tp) - 0 samples 


Thread: 17 (tp_osd_tp) - 0 samples 


Thread: 18 (tp_osd_tp) - 0 samples 


Thread: 19 (tp_osd_tp) - 0 samples 


Thread: 20 (tp_osd_tp) - 0 samples 


Thread: 21 (tp_osd_tp) - 0 samples 


Thread: 22 (tp_osd_tp) - 0 samples 


Thread: 23 (tp_osd_tp) - 0 samples 


Thread: 24 (tp_osd_tp) - 0 samples 


Thread: 25 (tp_osd_tp) - 0 samples 


Thread: 26 (tp_osd_tp) - 0 samples 


Thread: 27 (tp_osd_tp) - 0 samples 


Thread: 28 (tp_osd_tp) - 0 samples 


Thread: 29 (tp_peering) - 0 samples 


Thread: 30 (tp_peering) - 0 samples 


Thread: 31 (safe_timer) - 0 samples 


Thread: 32 (fn_anonymous) - 0 samples 


Thread: 33 (safe_timer) - 0 samples 


Thread: 34 (ms_local) - 0 samples 


Thread: 35 (ms_dispatch) - 0 samples 


Thread: 36 (ms_local) - 0 samples 


Thread: 37 (ms_dispatch) - 0 samples 


Thread: 38 (ms_local) - 0 samples 


Thread: 39 (ms_dispatch) - 0 samples 


Thread: 40 (ms_local) - 0 samples 


Thread: 41 (ms_dispatch) - 0 samples 


Thread: 42 (ms_local) - 0 samples 


Thread: 43 (ms_dispatch) - 0 samples 


Thread: 44 (ms_local) - 0 samples 


Thread: 45 (ms_dispatch) - 0 samples 


Thread: 46 (ms_local) - 0 samples 


Thread: 47 (ms_dispatch) - 0 samples 


Thread: 48 (bstore_mempool) - 0 samples 


Thread: 49 (bstore_kv_final) - 100 samples 

+ 100.00% clone
  + 100.00% start_thread
    + 100.00% BlueStore::KVFinalizeThread::entry
      + 100.00% BlueStore::_kv_finalize_thread
        + 65.00% std::condition_variable::wait(std::unique_lock<std::mutex>&)
        | + 65.00% pthread_cond_wait@@GLIBC_2.3.2
        + 22.00% BlueStore::deferred_try_submit
        | + 20.00% BlueStore::_deferred_submit_unlock
        | | + 16.00% KernelDevice::aio_submit
        | | | + 16.00% aio_queue_t::submit_batch
        | | |   + 16.00% io_submit
        | | + 3.00% KernelDevice::aio_write
        | | | + 1.00% should_gather
        | | | + 1.00% push_back
        | | | | + 1.00% _M_insert<aio_t>
        | | | |   + 1.00% _M_create_node<aio_t>
        | | | |     + 1.00% construct<std::_List_node<aio_t>, aio_t>
        | | | |       + 1.00% _List_node<aio_t>
        | | | |         + 1.00% aio_t
        | | | |           + 1.00% ceph::buffer::list::list(ceph::buffer::list&&)
        | | | |             + 1.00% ceph::buffer::list::iterator_impl<false>::advance
        | | | + 1.00% prepare_iov<boost::container::small_vector<iovec, 4ul> >
        | | + 1.00% PerfCounters::inc
        | + 1.00% std::vector<boost::intrusive_ptr<BlueStore::OpSequencer>, std::allocator<boost::intrusive_ptr<BlueStore::OpSequencer> > >::reserve
        |   + 1.00% capacity
        + 11.00% BlueStore::_txc_state_proc
        | + 7.00% BlueStore::_txc_finish
        | | + 3.00% BlueStore::BufferSpace::finish_write
        | | | + 3.00% erase
        | | |   + 3.00% std::_Rb_tree<unsigned int, std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > >, std::_Select1st<std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > > >, std::less<unsigned int>, mempool::pool_allocator<(mempool::pool_index_t)4, std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > > > >::erase
        | | |     + 3.00% erase
        | | |       + 3.00% _M_erase_aux
        | | |         + 3.00% clear
        | | |           + 3.00% std::_Rb_tree<unsigned int, std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > >, std::_Select1st<std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > > >, std::less<unsigned int>, mempool::pool_allocator<(mempool::pool_index_t)4, std::pair<unsigned int const, std::unique_ptr<BlueStore::Buffer, std::default_delete<BlueStore::Buffer> > > > >::_M_erase
        | | |             + 3.00% _M_destroy_node
        | | |               + 2.00% destroy
        | | |               | + 2.00% ~_Rb_tree_node
        | | |               |   + 2.00% ~pair
        | | |               |     + 2.00% ~unique_ptr
        | | |               |       + 2.00% operator()
        | | |               |         + 1.00% ~Buffer
        | | |               |         | + 1.00% ~list
        | | |               |         |   + 1.00% ~list
        | | |               |         |     + 1.00% ~_List_base
        | | |               |         |       + 1.00% std::_List_base<ceph::buffer::ptr, std::allocator<ceph::buffer::ptr> >::_M_clear
        | | |               |         |         + 1.00% destroy<std::_List_node<ceph::buffer::ptr> >
        | | |               |         |           + 1.00% ~_List_node
        | | |               |         + 1.00% BlueStore::Buffer::operator delete
        | | |               |           + 1.00% deallocate
        | | |               |             + 1.00% operator-=
        | | |               + 1.00% _M_put_node
        | | |                 + 1.00% deallocate
        | | |                   + 1.00% tc_deletearray
        | | + 2.00% BlueStore::TransContext::~TransContext
        | | | + 2.00% ~TransContext
        | | |   + 1.00% ~bluestore_deferred_transaction_t
        | | |   | + 1.00% ~list
        | | |   |   + 1.00% ~_List_base
        | | |   |     + 1.00% std::_List_base<bluestore_deferred_op_t, std::allocator<bluestore_deferred_op_t> >::_M_clear
        | | |   |       + 1.00% destroy<std::_List_node<bluestore_deferred_op_t> >
        | | |   |         + 1.00% ~_List_node
        | | |   |           + 1.00% ~bluestore_deferred_op_t
        | | |   |             + 1.00% ~list
        | | |   |               + 1.00% ~list
        | | |   |                 + 1.00% ~_List_base
        | | |   |                   + 1.00% std::_List_base<ceph::buffer::ptr, std::allocator<ceph::buffer::ptr> >::_M_clear
        | | |   |                     + 1.00% _M_put_node
        | | |   |                       + 1.00% deallocate
        | | |   |                         + 1.00% tc_delete
        | | |   |                           + 1.00% tcmalloc::ThreadCache::ListTooLong(tcmalloc::ThreadCache::FreeList*, unsigned long)
        | | |   |                             + 1.00% tcmalloc::ThreadCache::ReleaseToCentralCache(tcmalloc::ThreadCache::FreeList*, unsigned long, int)
        | | |   + 1.00% ~IOContext
        | | |     + 1.00% pthread_cond_destroy@@GLIBC_2.3.2
        | | + 1.00% tc_deletearray
        | | | + 1.00% tcmalloc::ThreadCache::ListTooLong(tcmalloc::ThreadCache::FreeList*, unsigned long)
        | | |   + 1.00% tcmalloc::ThreadCache::ReleaseToCentralCache(tcmalloc::ThreadCache::FreeList*, unsigned long, int)
        | | + 1.00% end
        | |   + 1.00% end
        | + 3.00% BlueStore::_txc_committed_kv
        | | + 2.00% queue
        | | | + 1.00% push_back
        | | | | + 1.00% std::vector<Context*, std::allocator<Context*> >::_M_emplace_back_aux<Context* const&>
        | | | + 1.00% Mutex::Lock
        | | |   + 1.00% pthread_mutex_lock
        | | |     + 1.00% _L_lock_791
        | | |       + 1.00% __lll_lock_wait
        | | + 1.00% tc_delete
        | + 1.00% log_state_latency
        |   + 1.00% ceph_clock_now
        + 2.00% BlueStore::DeferredBatch::~DeferredBatch
          + 2.00% ~DeferredBatch
            + 2.00% ~IOContext
              + 2.00% ~list
                + 2.00% ~_List_base
                  + 2.00% std::_List_base<aio_t, std::allocator<aio_t> >::_M_clear
                    + 2.00% destroy<std::_List_node<aio_t> >
                      + 2.00% ~_List_node
                        + 2.00% ~aio_t
                          + 2.00% ~list
                            + 2.00% ~list
                              + 2.00% ~_List_base
                                + 2.00% std::_List_base<ceph::buffer::ptr, std::allocator<ceph::buffer::ptr> >::_M_clear
                                  + 1.00% destroy<std::_List_node<ceph::buffer::ptr> >
                                  | + 1.00% ~_List_node
                                  |   + 1.00% ~ptr
                                  |     + 1.00% ceph::buffer::ptr::release
                                  |       + 1.00% ceph::buffer::raw_posix_aligned::~raw_posix_aligned
                                  |         + 1.00% ~raw_posix_aligned
                                  |           + 1.00% ~raw
                                  |             + 1.00% ~map
                                  |               + 1.00% ~_Rb_tree
                                  |                 + 1.00% std::_Rb_tree<std::pair<unsigned long, unsigned long>, std::pair<std::pair<unsigned long, unsigned long> const, std::pair<unsigned int, unsigned int> >, std::_Select1st<std::pair<std::pair<unsigned long, unsigned long> const, std::pair<unsigned int, unsigned int> > >, std::less<std::pair<unsigned long, unsigned long> >, std::allocator<std::pair<std::pair<unsigned long, unsigned long> const, std::pair<unsigned int, unsigned int> > > >::_M_erase
                                  |                   + 1.00% _M_destroy_node
                                  |                     + 1.00% _M_put_node
                                  |                       + 1.00% deallocate
                                  |                         + 1.00% tc_delete
                                  |                           + 1.00% tcmalloc::ThreadCache::ListTooLong(tcmalloc::ThreadCache::FreeList*, unsigned long)
                                  |                             + 1.00% tcmalloc::ThreadCache::ReleaseToCentralCache(tcmalloc::ThreadCache::FreeList*, unsigned long, int)
                                  + 1.00% _M_put_node
                                    + 1.00% deallocate
                                      + 1.00% tc_delete
                                        + 1.00% tcmalloc::ThreadCache::ListTooLong(tcmalloc::ThreadCache::FreeList*, unsigned long)
                                          + 1.00% tcmalloc::ThreadCache::ReleaseToCentralCache(tcmalloc::ThreadCache::FreeList*, unsigned long, int)

Thread: 50 (bstore_kv_sync) - 100 samples 

+ 100.00% clone
  + 100.00% start_thread
    + 100.00% BlueStore::KVSyncThread::entry
      + 100.00% BlueStore::_kv_sync_thread
        + 69.00% RocksDBStore::submit_transaction
        | + 69.00% RocksDBStore::submit_common
        |   + 69.00% rocksdb::DBImpl::Write
        |     + 69.00% rocksdb::DBImpl::WriteImpl
        |       + 36.00% rocksdb::DBImpl::WriteToWAL
        |       | + 36.00% rocksdb::DBImpl::WriteToWAL
        |       |   + 35.00% rocksdb::log::Writer::AddRecord
        |       |   | + 35.00% rocksdb::log::Writer::EmitPhysicalRecord
        |       |   |   + 26.00% rocksdb::crc32c::ExtendImpl<rocksdb::crc32c::Slow_CRC32>
        |       |   |   | + 26.00% Slow_CRC32
        |       |   |   + 8.00% rocksdb::WritableFileWriter::Append
        |       |   |     + 8.00% rocksdb::WritableFileWriter::WriteBuffered
        |       |   |       + 8.00% BlueRocksWritableFile::Append
        |       |   |         + 8.00% append
        |       |   |           + 8.00% append
        |       |   |             + 8.00% memcpy
        |       |   |               + 8.00% __memcpy_ssse3_back
        |       |   + 1.00% back
        |       |     + 1.00% end
        |       |       + 1.00% _Deque_iterator
        |       + 31.00% rocksdb::WriteBatchInternal::InsertInto
        |       | + 31.00% rocksdb::WriteBatch::Iterate
        |       |   + 30.00% rocksdb::MemTableInserter::PutCF
        |       |   | + 29.00% rocksdb::MemTable::Add
        |       |   | | + 21.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::Insert<false>
        |       |   | | | + 21.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::RecomputeSpliceLevels
        |       |   | | |   + 21.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::FindSpliceForLevel
        |       |   | | |     + 20.00% KeyIsAfterNode
        |       |   | | |       + 20.00% rocksdb::MemTable::KeyComparator::operator()
        |       |   | | |         + 11.00% rocksdb::InternalKeyComparator::Compare
        |       |   | | |         | + 9.00% rocksdb::(anonymous namespace)::BytewiseComparatorImpl::Compare
        |       |   | | |         |   + 9.00% compare
        |       |   | | |         |     + 9.00% __memcmp_sse4_1
        |       |   | | |         + 7.00% GetLengthPrefixedSlice
        |       |   | | + 7.00% __memcpy_ssse3_back
        |       |   | | + 1.00% rocksdb::EncodeVarint32
        |       |   | + 1.00% SeekToColumnFamily
        |       |   |   + 1.00% rocksdb::ColumnFamilyMemTablesImpl::Seek
        |       |   |     + 1.00% rocksdb::ColumnFamilySet::GetDefault
        |       |   + 1.00% rocksdb::MemTableInserter::DeleteCF
        |       |     + 1.00% DeleteImpl
        |       |       + 1.00% rocksdb::MemTable::Add
        |       |         + 1.00% rocksdb::(anonymous namespace)::SkipListRep::Allocate
        |       |           + 1.00% AllocateKey
        |       |             + 1.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::AllocateNode
        |       |               + 1.00% StashHeight
        |       + 1.00% rocksdb::InstrumentedMutex::Lock
        |       + 1.00% rocksdb::DBImpl::PreprocessWrite
        + 24.00% RocksDBStore::submit_transaction_sync
        | + 24.00% RocksDBStore::submit_common
        |   + 24.00% rocksdb::DBImpl::Write
        |     + 24.00% rocksdb::DBImpl::WriteImpl
        |       + 21.00% rocksdb::DBImpl::WriteToWAL
        |       | + 21.00% rocksdb::WritableFileWriter::Sync
        |       |   + 21.00% rocksdb::WritableFileWriter::SyncInternal
        |       |     + 21.00% BlueRocksWritableFile::Sync
        |       |       + 21.00% fsync
        |       |         + 21.00% BlueFS::_fsync
        |       |           + 19.00% BlueFS::_flush_bdev_safely
        |       |           | + 19.00% BlueFS::wait_for_aio
        |       |           |   + 19.00% IOContext::aio_wait
        |       |           |     + 19.00% std::condition_variable::wait(std::unique_lock<std::mutex>&)
        |       |           |       + 19.00% pthread_cond_wait@@GLIBC_2.3.2
        |       |           |         + 1.00% __pthread_mutex_cond_lock
        |       |           |           + 1.00% _L_cond_lock_792
        |       |           |             + 1.00% __lll_lock_wait
        |       |           + 2.00% BlueFS::_flush
        |       |             + 2.00% BlueFS::_flush_range
        |       |               + 2.00% KernelDevice::aio_submit
        |       |                 + 2.00% aio_queue_t::submit_batch
        |       |                   + 2.00% io_submit
        |       + 2.00% rocksdb::DBImpl::MarkLogsSynced
        |       | + 1.00% SignalAll
        |       |   + 1.00% rocksdb::port::CondVar::SignalAll
        |       + 1.00% rocksdb::WriteBatchInternal::InsertInto
        |         + 1.00% rocksdb::WriteBatch::Iterate
        |           + 1.00% rocksdb::MemTableInserter::SingleDeleteCF
        |             + 1.00% DeleteImpl
        |               + 1.00% rocksdb::MemTable::Add
        |                 + 1.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::Insert<false>
        |                   + 1.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::RecomputeSpliceLevels
        |                     + 1.00% rocksdb::InlineSkipList<rocksdb::MemTableRep::KeyComparator const&>::FindSpliceForLevel
        |                       + 1.00% KeyIsAfterNode
        |                         + 1.00% rocksdb::MemTable::KeyComparator::operator()
        |                           + 1.00% rocksdb::InternalKeyComparator::Compare
        |                             + 1.00% rocksdb::(anonymous namespace)::BytewiseComparatorImpl::Compare
        + 2.00% std::condition_variable::wait(std::unique_lock<std::mutex>&)
        | + 2.00% pthread_cond_wait@@GLIBC_2.3.2
        + 2.00% BlueStore::_txc_applied_kv
        + 1.00% operator std::__atomic_base<int>::__int_type
          + 1.00% load

Thread: 51 (finisher) - 0 samples 


Thread: 52 (dfin) - 0 samples 


Thread: 53 (rocksdb:bg0) - 0 samples 


Thread: 54 (rocksdb:bg0) - 0 samples 


Thread: 55 (bstore_aio) - 0 samples 


Thread: 56 (bstore_aio) - 0 samples 


Thread: 57 (bstore_aio) - 0 samples 


Thread: 58 (bstore_aio) - 0 samples 


Thread: 59 (safe_timer) - 0 samples 


Thread: 60 (safe_timer) - 0 samples 


Thread: 61 (safe_timer) - 0 samples 


Thread: 62 (safe_timer) - 0 samples 


Thread: 63 (ceph-osd) - 0 samples 


Thread: 64 (admin_socket) - 0 samples 


Thread: 65 (service) - 0 samples 


Thread: 66 (msgr-worker-2) - 0 samples 


Thread: 67 (msgr-worker-1) - 0 samples 


Thread: 68 (msgr-worker-0) - 0 samples 


Thread: 69 (log) - 0 samples 
```
