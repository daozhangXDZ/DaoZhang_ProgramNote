# ParallelFor Info

2019年2月27日

9:59

@author : white sma trail

 

| Source:                                                      | **ParallelFor.h** |      |
| ------------------------------------------------------------ | ----------------- | ---- |
|                                                              |                   |      |
| `inline   void ParallelFor(int32 Num, TFunctionRef<void(int32)> Body, bool   bForceSingleThread = false)`   `{`   `SCOPE_CYCLE_COUNTER(STAT_ParallelFor);`   `check(Num   >= 0);`   ` `   `int32   AnyThreadTasks = 0;`   `if   (Num > 1 && !bForceSingleThread &&   FApp::ShouldUseThreadingForPerformance())`   `{`   `AnyThreadTasks   = FMath::Min<int32>(FTaskGraphInterface::Get().GetNumWorkerThreads(),   Num - 1);`   `}`   `if   (!AnyThreadTasks)`   `{`   `// no   threads, just do it and return`   `for   (int32 Index = 0; Index < Num; Index++)`   `{`   `Body(Index);`   `}`   `return;`   `}`   `FParallelForData*   DataPtr = new FParallelForData(Num, AnyThreadTasks + 1, Num >   AnyThreadTasks + 1, Body);`   `TSharedRef<FParallelForData,   ESPMode::ThreadSafe> Data = MakeShareable(DataPtr);`   `TGraphTask<FParallelForTask>::CreateTask().ConstructAndDispatchWhenReady(Data,   AnyThreadTasks -   1);                `   `//   this thread can help too and this is important to prevent deadlock on   recursion `   `if   (!Data->Process(0, Data, true))`   `{`   `Data->Event->Wait();`   `check(Data->bTriggered);`   `}`   `else`   `{`   `check(!Data->bTriggered);`   `}`   `check(Data->NumCompleted.GetValue()   == Data->Num);`   `Data->bExited   = true;`   `//   DoneEvent waits here if some other thread finishes the last item`   `//   Data must live on until all of the tasks are cleared which might be long   after this function exits`   `}` |                   |      |

 

 

TFunctionRef

2019年2月27日

10:01
